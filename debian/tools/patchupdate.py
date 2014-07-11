#!/usr/bin/python
from multiprocessing import Pool
from xml.dom import minidom
import contextlib
import textwrap
import urllib
import sys
import os
import re

class AuthorInfo(object):
    def __init__(self):
        self.author = ""
        self.subject = ""
        self.revision = ""

class PatchSet(object):
    def __init__(self, name):
        self.name    = name
        self.authors = []
        self.fixes   = []
        self.changes = []

        self.patches = []
        self.files   = set()
        self.depends = set()

        self.verify_depends = set()
        self.verify_time    = None

def pairs(a):
    for i, j in enumerate(a):
        for k in a[i+1:]:
            yield (j, k)

def causal_time_combine(a, b):
    return [(a if a > b else b) for a, b in zip(a, b)]

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
            print "** Found circular dependencies, unable to apply remaining patches:"
            print "** %s" % ", ".join([patch.name for dummy, patch in patches.iteritems()])
            exit(1)

        for j in to_delete:
            for i, patch in patches.iteritems():
                if i != j and j in patch.verify_depends:
                    patch.verify_time = causal_time_combine(patch.verify_time, patches[j].verify_time)
                    patch.verify_depends.remove(j)
            del patches[j]

    # Find out which files are modified by multiple patches
    modified_files = {}
    for i, patch in all_patches.iteritems():
        for f in patch.files:
            if f not in modified_files:
                modified_files[f] = []
            modified_files[f].append(i)

    # Iterate over pairs of patches, check for existing causal relationship
    for f, indices in modified_files.iteritems():
        for i, j in pairs(indices):
            if not causal_time_relation(all_patches[i].verify_time, all_patches[j].verify_time):
                print "** Missing dependency between %s and %s" % (all_patches[i].name, all_patches[j].name)
                print "** Both patches modify the same file %s" % f
                exit(1)

def lsdiff(f):
    with open(f) as fp:
        for line in fp:
            if line.startswith("diff --git "):
                tmp = line.strip().split(" ")
                if len(tmp) == 4 and tmp[3].startswith("b/"):
                    yield tmp[3][2:]

def download(url):
    with contextlib.closing(urllib.urlopen(url)) as wr:
        return wr.read()

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

            # Append to the list of patches within this set
            patch.patches.append(f)

            # Determine which files are affected
            for modified_file in lsdiff(os.path.join(subdirectory, f)):
                patch.files.add(modified_file)

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
            print "** Missing definition file: %s" % deffile
            exit(1)

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
                        print "** Definition file %s references unknown dependency %s" % (deffile, val)
                        exit(1)
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

        depends = " ".join([""] + ["%s.ok" % patches[d].name for d in patch.depends]) if len(patch.depends) else ""
        fp.write("%s.ok:%s\n" % (patch.name, depends))
        for f in patch.patches:
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

def generate_readme(patches, fp):
    fp.write("wine-compholio\n")
    fp.write("==============\n")
    fp.write("\n")
    fp.write("The Wine \"Compholio\" Edition repository includes a variety of patches ")
    fp.write("for Wine to run common Windows applications under Linux.\n")
    fp.write("\n")
    fp.write("These patches fix the following Wine bugs:\n")
    fp.write("\n")

    all_bugs = []
    for i, patch in patches.iteritems():
        for (bugid, bugname, description) in patch.fixes:
            if bugid is not None: all_bugs.append((bugid, bugname, description))
    for (bugid, bugname, description) in sorted(all_bugs):
        if description is None: description = bugname
        fp.write("* %s ([Wine Bug #%d](http://bugs.winehq.org/show_bug.cgi?id=%d \"%s\"))\n" % (description, bugid, bugid, bugname))

    fp.write("\n")
    fp.write("\n")
    fp.write("Besides that the following additional changes are included:\n")
    fp.write("\n")

    all_fixes = []
    for i, patch in patches.iteritems():
        for (bugid, bugname, description) in patch.fixes:
            if bugid is None: all_fixes.append(description)
    for description in sorted(all_fixes):
        fp.write("* %s\n" % description)

    fp.write("\n")

if __name__ == "__main__":
    patches = read_patchsets("./patches")
    verify_dependencies(patches)

    with open("./patches/Makefile", "w") as fp:
        generate_makefile(patches, fp)

    with open("./README.md", "w") as fp:
        generate_readme(patches, fp)
