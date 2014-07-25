#!/usr/bin/python
from multiprocessing import Pool
from xml.dom import minidom
import contextlib
import textwrap
import urllib
import sys
import hashlib
import itertools
import patchutils
import os
import re

class AuthorInfo(object):
    def __init__(self):
        self.author         = ""
        self.subject        = ""
        self.revision       = ""

class PatchSet(object):
    def __init__(self, name):
        self.name           = name
        self.authors        = []
        self.fixes          = []
        self.changes        = []

        self.files          = []
        self.patches        = []
        self.modified_files = set()
        self.depends        = set()

        self.verify_depends = set()
        self.verify_time    = None

def abort(m):
    print "*** CRITICAL ERROR ***"
    print m
    exit(1)

def pairs(a):
    for i, j in enumerate(a):
        for k in a[i+1:]:
            yield (j, k)

def causal_time_combine(a, b):
    return [max(a, b) for a, b in zip(a, b)]

def causal_time_smaller(a, b):
    return all([i <= j for i, j in zip(a,b)]) and any([i < j for i, j in zip(a,b)])

def causal_time_relation(a, b):
    return causal_time_smaller(a, b) or causal_time_smaller(b, a)

def verify_dependencies(all_patches):
    max_patches = max(all_patches.keys()) + 1

    for i, patch in all_patches.iteritems():
        patch.verify_depends = set(patch.depends)
        patch.verify_time    = [0]*max_patches

    # Check for circular dependencies and perform modified vector clock algorithm
    patches = dict(all_patches)
    while len(patches):

        to_delete = []
        for i, patch in patches.iteritems():
            if len(patch.verify_depends) == 0:
                patch.verify_time[i] += 1
                to_delete.append(i)

        if len(to_delete) == 0:
            abort("Circular dependency in set of patches: %s" % ", ".join([patch.name for dummy, patch in patches.iteritems()]))

        for j in to_delete:
            for i, patch in patches.iteritems():
                if i != j and j in patch.verify_depends:
                    patch.verify_time = causal_time_combine(patch.verify_time, patches[j].verify_time)
                    patch.verify_depends.remove(j)
            del patches[j]

    # Find out which files are modified by multiple patches
    modified_files = {}
    for i, patch in all_patches.iteritems():
        for f in patch.modified_files:
            if f not in modified_files:
                modified_files[f] = []
            modified_files[f].append(i)

    # Iterate over pairs of patches, check for existing causal relationship
    for f, indices in modified_files.iteritems():
        for i, j in pairs(indices):
            if not causal_time_relation(all_patches[i].verify_time, all_patches[j].verify_time):
                abort("Missing dependency between %s and %s because of same file %s" % (all_patches[i].name, all_patches[j].name, f))

def download(url):
    with contextlib.closing(urllib.urlopen(url)) as fp:
        return fp.read()

def read_patchsets(directory):
    next_patch = 0
    patches = {}
    name_to_id = {}
    all_bugs = []

    for name in sorted(os.listdir(directory)): # Read in sorted order to ensure created Makefile doesn't change too much
        if name in [".", ".."]: continue
        subdirectory = os.path.join(directory, name)
        if not os.path.isdir(subdirectory): continue

        patch = PatchSet(name)

        for f in sorted(os.listdir(subdirectory)):
            if not f.endswith(".patch") or not os.path.isfile(os.path.join(subdirectory, f)):
                continue
            patch.files.append(f)
            for p in patchutils.read_patch(os.path.join(subdirectory, f)):
                patch.patches.append(p)
                patch.modified_files.add(p.modified_file)

        # No single patch within this directory, ignore it
        if len(patch.patches) == 0:
            del patch
            continue

        patches[next_patch] = patch
        name_to_id[name] = next_patch
        next_patch += 1

    # Now read the definition files in a second step
    for i, patch in patches.iteritems():
        deffile = os.path.join(os.path.join(directory, patch.name), "definition")

        if not os.path.isfile(deffile):
            abort("Missing definition file %s" % deffile)

        info = AuthorInfo()

        with open(deffile) as fp:
            for line in fp:
                if line.startswith("#"): continue
                tmp = line.split(":", 1)
                if len(tmp) < 2:
                    if len(info.author) and len(info.subject) and len(info.revision):
                        patch.authors.append(info)
                        info = AuthorInfo()
                    continue
                cmd = tmp[0].lower()
                val = tmp[1].strip()

                if cmd == "author":
                    if len(info.author): info.author += ", "
                    info.author += val
                elif cmd == "subject" or cmd == "title":
                    if len(info.subject): info.subject += " "
                    info.subject += val
                elif cmd == "revision":
                    if len(info.revision): info.revision += ", "
                    info.revision += val
                elif cmd == "fixes":
                    r = re.match("^[0-9]+$", val)
                    if r:
                        bugid = int(val)
                        patch.fixes.append((bugid, None, None))
                        all_bugs.append(bugid)
                        continue
                    r = re.match("^\\[ *([0-9]+) *\\](.*)$", val)
                    if r:
                        bugid, description = int(r.group(1)), r.group(2).strip()
                        patch.fixes.append((bugid, None, description))   
                        all_bugs.append(bugid)
                        continue
                    patch.fixes.append((None, None, val))
                elif cmd == "depends":
                    if not name_to_id.has_key(val):
                        abort("Definition file %s references unknown dependency %s" % (deffile, val))
                    patch.depends.add(name_to_id[val])
                else:
                    print "** Ignoring unknown command in definition file %s: %s" % (deffile, line)

            if len(info.author) and len(info.subject) and len(info.revision):
                patch.authors.append(info)

    # In a third step query information for the patches from Wine bugzilla
    pool = Pool(8)
    bug_short_desc = {None:None}
    for bugid, data in zip(all_bugs, pool.map(download, ["http://bugs.winehq.org/show_bug.cgi?id=%d&ctype=xml&field=short_desc" % bugid for bugid in all_bugs])):
        bug_short_desc[bugid] = minidom.parseString(data).getElementsByTagName('short_desc')[0].firstChild.data
    pool.close()
    for i, patch in patches.iteritems():
        patch.fixes = [(bugid, bug_short_desc[bugid], description) for bugid, dummy, description in patch.fixes]

    return patches

def read_changelog():
    with open("debian/changelog") as fp:
        for line in fp:
            r = re.match("^([a-zA-Z0-9][^(]*)\((.*)\) ([^;]*)", line)
            if r: yield (r.group(1).strip(), r.group(2).strip(), r.group(3).strip())

def generate_makefile(patches, fp):
    fp.write("#\n")
    fp.write("# This file is automatically generated, DO NOT EDIT!\n")
    fp.write("#\n")
    fp.write("\n")
    fp.write("CURDIR ?= ${.CURDIR}\n")
    fp.write("PATCH := $(CURDIR)/../debian/tools/gitapply.sh -d $(DESTDIR)\n")
    fp.write("\n")
    fp.write("PATCHLIST :=\t%s\n" % " \\\n\t\t".join(["%s.ok" % patch.name for i, patch in patches.iteritems()]))
    fp.write("\n")
    fp.write(".PHONY: install\n")
    fp.write("install: $(PATCHLIST)\n")
    fp.write("\tcat *.ok | sort | $(CURDIR)/../debian/tools/patchlist.sh | $(PATCH)\n")
    fp.write("\tcd $(DESTDIR); autoreconf -f\n")
    fp.write("\tcd $(DESTDIR); ./tools/make_requests\n")
    fp.write("\trm -f *.ok\n")
    fp.write("\n")
    fp.write(".PHONY: abort\n")
    fp.write("abort:\n")
    fp.write("\trm -f *.ok\n")
    fp.write("\n")
    fp.write(".NOTPARALLEL:\n")
    fp.write("\n")

    for i, patch in patches.iteritems():
        fp.write("# Patchset %s\n" % patch.name)
        fp.write("# |\n")
        fp.write("# | Included patches:\n")
        for info in patch.authors:
            if not info.subject: continue
            s = []
            if info.revision and info.revision != "1": s.append("rev %s" % info.revision)
            if info.author: s.append("by %s" % info.author)
            if len(s): s = " [%s]" % ", ".join(s)
            fp.write("# |   *\t%s\n" % "\n# | \t".join(textwrap.wrap(info.subject + s, 120)))
        fp.write("# |\n")

        if any([bugid is not None for bugid, bugname, description in patch.fixes]):
            fp.write("# | This patchset fixes the following Wine bugs:\n")
            for bugid, bugname, description in patch.fixes:
                if bugid is not None:
                    fp.write("# |   *\t%s\n" % "\n# | \t".join(textwrap.wrap("[#%d] %s" % (bugid, bugname), 120)))
            fp.write("# |\n")

        fp.write("# | Modified files: \n")
        fp.write("# |   *\t%s\n" % "\n# | \t".join(textwrap.wrap(", ".join(sorted(patch.modified_files)), 120)))
        fp.write("# |\n")

        depends = " ".join([""] + ["%s.ok" % patches[d].name for d in patch.depends]) if len(patch.depends) else ""
        fp.write("%s.ok:%s\n" % (patch.name, depends))
        for f in patch.files:
            fp.write("\t$(PATCH) < %s\n" % os.path.join(patch.name, f))

        if len(patch.authors):
            fp.write("\t( \\\n")
            for info in patch.authors:
                if not info.subject: continue
                s = info.subject
                if info.revision and info.revision != "1": s += " [rev %s]" % info.revision
                fp.write("\t\techo \"+    { \\\"%s\\\", \\\"%s\\\", \\\"%s\\\" },\"; \\\n" % (patch.name, info.author, s))
            fp.write("\t) > %s.ok\n" % patch.name)
        else:
            fp.write("\ttouch %s.ok\n" % patch.name)
        fp.write("\n");

README_template = """wine-compholio
==============

The Wine \"Compholio\" Edition repository includes a variety of patches ") for
Wine to run common Windows applications under Linux.

These patches fix the following Wine bugs:

{bugs}

Besides that the following additional changes are included:

{fixes}

### Compiling wine-compholio

In order to wine-compholio, please use the recommended Makefile based approach which
will automatically decide whether to use 'git apply' or 'gitapply.sh'. The following
instructions (based on the [Gentoo Wiki](https://wiki.gentoo.org/wiki/Netflix/Pipelight#Compiling_manually))
will give a short overview how to compile wine-compholio, but of course not explain
details. Make sure to install all required wine dependencies before proceeding.

As the first step please grab the latest Wine source:
```bash
wget http://prdownloads.sourceforge.net/wine/wine-{version}.tar.bz2
wget https://github.com/compholio/wine-compholio-daily/archive/v{version}.tar.gz
```
Extract the archives:
```bash
tar xvjf wine-1*.tar.bz2
cd wine-1*
tar xvzf ../v{version}.tar.gz --strip-components 1
```
And apply the patches:
```bash
make -C ./patches DESTDIR=$(pwd) install
```
Afterwards run configure (you can also specify a prefix if you don't want to install
wine-compholio system-wide):
```bash
./configure --with-xattr
```
Before you continue you should make sure that ./configure doesn't show any warnings
(look at the end of the output). If there are any warnings, this most likely means
that you're missing some important header files. Install them and repeat the ./configure
step until all problems are fixed.

Afterwards compile it (and grab a cup of coffee):
```bash
make
```
And install it (you only need sudo for a system-wide installation):
```bash
sudo make install
```

### Excluding patches

It is also possible to apply only a subset of the patches, for example if you're compiling
for a distribution where PulseAudio is not installed, or if you just don't like a specific
patchset. Please note that some patchsets depend on each other, and requesting an impossible
situation might result in a failure to apply all patches.

Lets assume you want to exclude the patchset in directory DIRNAME, then just invoke make like that:
```bash
make -C ./patches DESTDIR=$(pwd) install -W DIRNAME.ok
```
"""

def generate_readme(patches, fp):

    def _all_bugs():
        all_bugs = []
        for i, patch in patches.iteritems():
            for (bugid, bugname, description) in patch.fixes:
                if bugid is not None: all_bugs.append((bugid, bugname, description))
        for (bugid, bugname, description) in sorted(all_bugs):
            if description is None: description = bugname
            yield "%s ([Wine Bug #%d](http://bugs.winehq.org/show_bug.cgi?id=%d \"%s\"))" % (description, bugid, bugid, bugname)

    def _all_fixes():
        all_fixes = []
        for i, patch in patches.iteritems():
            for (bugid, bugname, description) in patch.fixes:
                if bugid is None: all_fixes.append(description)
        for description in sorted(all_fixes):
            yield description

    def _enum(x):
        return "* " + "\n* ".join(x)

    def _latest_stable_version():
        for package, version, distro in read_changelog():
            if distro.lower() == "unreleased": continue
            return version

    fp.write(README_template.format(bugs=_enum(_all_bugs()), fixes=_enum(_all_fixes()), version=_latest_stable_version()))

if __name__ == "__main__":
    patches = read_patchsets("./patches")
    verify_dependencies(patches)

    with open("./patches/Makefile", "w") as fp:
        generate_makefile(patches, fp)

    with open("./README.md", "w") as fp:
        generate_readme(patches, fp)
