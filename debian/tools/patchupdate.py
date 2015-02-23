#!/usr/bin/python2
#
# Automatic patch dependency checker and apply script/README.md generator.
#
# Copyright (C) 2014-2015 Sebastian Lackner
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301, USA
#

import binascii
import cPickle as pickle
import fnmatch
import hashlib
import itertools
import math
import multiprocessing.pool
import operator
import os
import patchutils
import progressbar
import re
import signal
import subprocess
import sys
import tempfile
import textwrap

_devnull = open(os.devnull, 'wb')

# Cached information to speed up patch dependency checks
latest_wine_commit  = None
cached_patch_result = {}

class config(object):
    path_patches            = "patches"
    path_changelog          = "debian/changelog"
    path_wine               = "debian/tools/wine"

    path_template_script    = "debian/tools/patchinstall.sh.in"
    path_script             = "patches/patchinstall.sh"

    path_template_README_md = "debian/tools/README.md.in"
    path_README_md          = "README.md"

    path_IfDefined          = "9999-IfDefined.patch"

class PatchUpdaterError(RuntimeError):
    """Failed to update patches."""
    pass

class PatchSet(object):
    def __init__(self, name, directory):
        self.name           = name
        self.variable       = None
        self.directory      = directory
        self.fixes          = []
        self.changes        = []
        self.disabled       = False
        self.ifdefined      = None

        self.files          = []
        self.patches        = []
        self.modified_files = set()
        self.depends        = set()
        self.auto_depends   = set()

        self.verify_time    = None

def _pairs(a):
    """Iterate over all pairs of elements contained in the list a."""
    for i, j in enumerate(a):
        for k in a[i+1:]:
            yield (j, k)

def _unique(iterable, key=None):
    "List unique elements, preserving order. Remember only the element just seen."
    # _unique('AAAABBBCCDAABBB') --> A B C D A B
    # _unique('ABBCcAD', str.lower) --> A B C A D
    return itertools.imap(next, itertools.imap(operator.itemgetter(1), itertools.groupby(iterable, key)))

def _split_seq(iterable, size):
    """Split an iterator into chunks of a given size."""
    it = iter(iterable)
    items = list(itertools.islice(it, size))
    while items:
        yield items
        items = list(itertools.islice(it, size))

def _escape(s):
    """Escape string inside of '...' quotes."""
    return s.replace("\\", "\\\\\\\\").replace("\"", "\\\"").replace("'", "'\\''")

def _load_dict(filename):
    """Load a Python dictionary object from a file."""
    try:
        with open(filename) as fp:
            return pickle.load(fp)
    except IOError:
        return {}

def _save_dict(filename, value):
    """Save a Python dictionary object to a file."""
    with open(filename, "wb") as fp:
        pickle.dump(value, fp, pickle.HIGHEST_PROTOCOL)

def _sha256(fp):
    """Calculate sha256sum from a file descriptor."""
    m = hashlib.sha256()
    fp.seek(0)
    while True:
        buf = fp.read(16384)
        if buf == "": break
        m.update(buf)
    return m.digest()

def _parse_int(val, default=0):
    """Parse an integer or boolean value."""
    r = re.match("^[0-9]+$", val)
    if r:
        return int(val)
    try:
        return {'true': 1, 'yes': 1, 'false': 0, 'no': 0}[val.lower()]
    except AttributeError:
        return default

def _read_changelog():
    """Read information from changelog."""
    with open(config.path_changelog) as fp:
        for line in fp:
            r = re.match("^([a-zA-Z0-9][^(]*)\((.*)\) ([^;]*)", line)
            if r: yield (r.group(1).strip(), r.group(2).strip(), r.group(3).strip())

def _stable_compholio_version():
    """Get version number of the latest stable release."""
    for package, version, distro in _read_changelog():
        if distro.lower() != "unreleased":
            return version

def _latest_wine_commit(commit=None):
    """Get latest wine commit."""
    if not os.path.isdir(config.path_wine):
        raise PatchUpdaterError("Please create a symlink to the wine repository in %s" % config.path_wine)
    if commit is None:
        commit = subprocess.check_output(["git", "rev-parse", "origin/master"], cwd=config.path_wine).strip()
    assert len(commit) == 40
    return commit

def enum_directories(revision, path):
    """Enumerate all subdirectories of 'path' at a specific revision."""
    dirs = []

    if path[0:2] == "./":
        path = path[2:]
    elif path[0] == "/":
        raise RuntimeError("Expected relative path, not an absolute path")

    if revision is None:
        for name in os.listdir(path):
            if name in [".", ".."]: continue
            directory = os.path.join(path, name)
            if not os.path.isdir(directory):
                continue
            dirs.append((name, directory))
    else:
        filename = "%s:%s" % (revision, path)
        try:
            content = subprocess.check_output(["git", "show", filename], stderr=_devnull)
        except subprocess.CalledProcessError as e:
            if e.returncode != 128: raise
            return [] # ignore error
        lines = content.split("\n")
        if not lines[0].startswith("tree ") or lines[1] != "":
            raise RuntimeError("Unexpected output from 'git show %s'" % filename)
        for name in lines[2:]:
            if name == "" or name[-1] != "/": continue
            name = name[:-1]
            dirs.append((name, os.path.join(path, name)))

    return dirs

def read_patchset(revision = None):
    """Read information about all patchsets for a specific revision."""
    unique_id   = itertools.count()
    all_patches = {}
    name_to_id  = {}

    # Read in sorted order (to ensure created Makefile doesn't change too much)
    for name, directory in sorted(enum_directories(revision, config.path_patches)):
        patch = PatchSet(name, directory)

        if revision is None:

            # If its the latest revision, then request additional information
            if not os.path.isdir(directory):
                raise RuntimeError("Unable to open directory %s" % directory)

            # Enumerate .patch files in the given directory, enumerate individual patches and affected files
            for f in sorted(os.listdir(directory)):
                if not re.match("^[0-9]{4}-.*\\.patch$", f):
                    continue
                if f.startswith(config.path_IfDefined):
                    continue
                if not os.path.isfile(os.path.join(directory, f)):
                    continue
                patch.files.append(f)
                for p in patchutils.read_patch(os.path.join(directory, f)):
                    patch.modified_files.add(p.modified_file)
                    patch.patches.append(p)

            # No single patch within this directory, ignore it
            if len(patch.patches) == 0:
                del patch
                continue

        i = next(unique_id)
        all_patches[i]   = patch
        name_to_id[name] = i

    # Now read the definition files in a second step
    for i, patch in all_patches.iteritems():
        try:
            filename = os.path.join(os.path.join(config.path_patches, patch.name), "definition")
            if revision is None:
                with open(filename) as fp:
                    content = fp.read()
            else:
                filename = "%s:%s" % (revision, filename)
                content = subprocess.check_output(["git", "show", filename], stderr=_devnull)
        except (IOError, subprocess.CalledProcessError):
            continue # Skip this definition file

        for line in content.split("\n"):
            if line.startswith("#"):
                continue
            tmp = line.split(":", 1)
            if len(tmp) != 2:
                continue

            key, val = tmp[0].lower(), tmp[1].strip()
            if key == "depends":
                if not name_to_id.has_key(val):
                    raise PatchUpdaterError("Definition file %s references unknown dependency %s" % (filename, val))
                patch.depends.add(name_to_id[val])

            elif key == "apply-after":
                for j, other_patch in all_patches.iteritems():
                    if i != j and any([fnmatch.fnmatch(f, val) for f in other_patch.modified_files]):
                        patch.auto_depends.add(j)

            elif key == "fixes":
                r = re.match("^[0-9]+$", val)
                if r:
                    patch.fixes.append((int(val), None))
                    continue
                r = re.match("^\\[ *([0-9]+) *\\](.*)$", val)
                if r:
                    patch.fixes.append((int(r.group(1)), r.group(2).strip()))
                    continue
                patch.fixes.append((None, val))

            elif key == "disabled":
                patch.disabled = _parse_int(val)

            elif key == "ifdefined":
                patch.ifdefined = val

            elif revision is None:
                print "WARNING: Ignoring unknown command in definition file %s: %s" % (filename, line)

    return all_patches

def causal_time_combine(a, b):
    """Combines two timestamps into a new one."""
    return [max(a, b) for a, b in zip(a, b)]

def causal_time_smaller(a, b):
    """Checks if timestamp a is smaller than timestamp b."""
    return all([i <= j for i, j in zip(a,b)]) and any([i < j for i, j in zip(a,b)])

def causal_time_relation(all_patches, indices):
    """Checks if the dependencies of patches are compatible with a specific apply order."""
    for i, j in _pairs(indices):
        if causal_time_smaller(all_patches[j].verify_time, all_patches[i].verify_time):
            return False
    return True

def causal_time_relation_any(all_patches, indices):
    """Similar to causal_time_relation(), but also check all possible permutations of indices."""
    for i, j in _pairs(indices):
        if not (causal_time_smaller(all_patches[i].verify_time, all_patches[j].verify_time) or \
                causal_time_smaller(all_patches[j].verify_time, all_patches[i].verify_time)):
            return False
    return True

def contains_binary_patch(all_patches, indices, filename):
    """Checks if any patch with given indices affecting filename is a binary patch."""
    for i in indices:
        for patch in all_patches[i].patches:
            if patch.modified_file == filename and patch.is_binary():
                return True
    return False

def get_wine_file(filename):
    """Return the hash and optionally the content of a file."""
    entry  = "%s:%s" % (latest_wine_commit, filename)
    result = tempfile.NamedTemporaryFile()
    try:
        content = subprocess.check_call(["git", "show", entry], cwd=config.path_wine, \
                                        stdout=result, stderr=_devnull)
    except subprocess.CalledProcessError as e:
        if e.returncode != 128: raise
    result.flush() # shouldn't be necessary because the subprocess writes directly to the fd
    return result

def extract_patch(patchset, filename):
    """Extract all changes to a specific file from a patchset."""
    p = tempfile.NamedTemporaryFile()
    m = hashlib.sha256()

    for patch in patchset.patches:
        if patch.modified_file != filename:
            continue
        for chunk in patch.read_chunks():
            p.write(chunk)
            m.update(chunk)
        p.write("\n")
        m.update("\n")

    p.flush()
    return (m.digest(), p)

def select_patches(all_patches, indices, filename):
    """Create a temporary patch file for each patchset and calculate the checksum."""
    selected_patches = {}
    for i in indices:
        selected_patches[i] = extract_patch(all_patches[i], filename)
    return selected_patches

def resolve_dependencies(all_patches, index = None, depends = None):
    """Returns a sorted list with all dependencies for a given patch."""

    def _resolve(depends):
        for i in depends:
            # Check for disabled patch
            if all_patches[i].disabled:
                raise PatchUpdaterError("Encountered dependency on disabled patchset %s" % all_patches[i].name)
            # Dependencies already resolved
            if all_patches[i].verify_resolved > 0:
                continue
            # Detect circular dependency
            if all_patches[i].verify_resolved < 0:
                raise PatchUpdaterError("Circular dependency while trying to resolve %s" % all_patches[i].name)

            # Recusively resolve dependencies
            all_patches[i].verify_resolved = -1
            _resolve(all_patches[i].depends)
            _resolve(all_patches[i].auto_depends)
            all_patches[i].verify_resolved = 1
            resolved.append(i)

    for _, patch in all_patches.iteritems():
        patch.verify_resolved = 0

    resolved = []
    if depends is None:
        depends = all_patches[index].depends
    _resolve(depends)
    return resolved

def generate_ifdefined(all_patches):
    """Update autogenerated ifdefined patches, which can be used to selectively disable features at compile time."""
    enabled_patches = dict([(i, patch) for i, patch in all_patches.iteritems() if not patch.disabled])

    for i, patch in enabled_patches.iteritems():
        if patch.ifdefined is None:
            continue

        filename = os.path.join(patch.directory, config.path_IfDefined)
        with open(filename, "wb") as fp:
            fp.write("From: Wine Staging Team <webmaster@fds-team.de>\n")
            fp.write("Subject: Autogenerated #ifdef patch for %s.\n" % patch.name)
            fp.write("\n")

            depends = resolve_dependencies(enabled_patches, i)
            for f in patch.modified_files:

                # Reconstruct the state after applying the dependencies
                original = get_wine_file(f)
                for _, (_, p) in select_patches(enabled_patches, depends, f).iteritems():
                    original = patchutils.apply_patch(original, p, fuzz=0)

                # Now apply the main patch
                p = extract_patch(patch, f)[1]
                patched = patchutils.apply_patch(original, p, fuzz=0)

                # Now get the diff between both
                diff = patchutils.generate_ifdef_patch(original, patched, ifdef=patch.ifdefined)
                if diff is not None:
                    fp.write("diff --git a/%s b/%s\n" % (f, f))
                    fp.write("--- a/%s\n" % f)
                    fp.write("+++ b/%s\n" % f)
                    while True:
                        buf = diff.read(16384)
                        if buf == "": break
                        fp.write(buf)
                    diff.close()

            # Close the file
            fp.close()

        # Add changes to git
        subprocess.call(["git", "add", filename])

        # Add the autogenerated file as a last patch
        patch.files.append(os.path.basename(filename))
        for p in patchutils.read_patch(filename):
            assert p.modified_file in patch.modified_files
            patch.patches.append(p)

def generate_script(all_patches):
    """Resolve dependencies, and afterwards check if everything applies properly."""
    depends     = sorted([i for i, patch in all_patches.iteritems() if not patch.disabled])
    resolved    = resolve_dependencies(all_patches, depends=depends)
    max_patches = max(resolved) + 1

    # Generate timestamps based on dependencies, still required for binary patches
    # Find out which files are modified by multiple patches
    modified_files = {}
    for i, patch in [(i, all_patches[i]) for i in resolved]:
        patch.verify_time = [0]*max_patches
        patch.verify_time[i] += 1
        for j in patch.depends:
            patch.verify_time = causal_time_combine(patch.verify_time, all_patches[j].verify_time)

        for f in patch.modified_files:
            if f not in modified_files:
                modified_files[f] = []
            modified_files[f].append(i)

    # Check dependencies
    pool = multiprocessing.pool.ThreadPool(processes=4)
    try:
        for filename, indices in modified_files.iteritems():

            # If one of patches is a binary patch, then we cannot / won't verify it - require dependencies in this case
            if contains_binary_patch(all_patches, indices, filename):
                if not causal_time_relation_any(all_patches, indices):
                    raise PatchUpdaterError("Because of binary patch modifying file %s the following patches need explicit dependencies: %s" %
                                            (filename, ", ".join([all_patches[i].name for i in indices])))
                continue

            original_content = get_wine_file(filename)
            selected_patches = select_patches(all_patches, indices, filename)

            # Show a progress bar while applying the patches - this task might take some time
            chunk_size = 20
            with progressbar.ProgressBar(desc=filename, total=2 ** len(indices) / chunk_size) as progress:

                def test_apply(bitstring):
                    set_apply = [(i, all_patches[i]) for u, i in zip(bitstring, indices) if u]
                    set_skip  = [(i, all_patches[i]) for u, i in zip(bitstring, indices) if not u]

                    # Check if there is any patch2 which depends directly or indirectly on patch1.
                    # If this is the case we found an impossible situation, we can be skipped in this test.
                    for i, patch1 in set_apply:
                        for j, patch2 in set_skip:
                            if causal_time_smaller(patch2.verify_time, patch1.verify_time):
                                return True # we can skip this test

                    try:
                        original = original_content
                        for i, patch in set_apply:
                            original = patchutils.apply_patch(original, selected_patches[i][1], fuzz=0)
                    except patchutils.PatchApplyError:
                        return False

                    return True # everything is fine

                def test_apply_seq(bitstrings):
                    for bitstring in bitstrings:
                        if not test_apply(bitstring):
                            return False
                    return True

                it = _split_seq(itertools.product([0,1], repeat=len(indices)), chunk_size)
                for k, res in enumerate(pool.imap_unordered(test_apply_seq, it)):
                    if not res:
                        progress.finish("<failed to apply>")
                        raise PatchUpdaterError("Changes to file %s don't apply: %s" %
                                                (filename, ", ".join([all_patches[i].name for i in indices])))
                    progress.update(k)
    finally:
        pool.close()

    # Generate code for helper functions
    lines = []
    lines.append("# Enable or disable all patchsets\n")
    lines.append("patch_enable_all ()\n")
    lines.append("{\n")
    for i, patch in sorted([(i, all_patches[i]) for i in resolved], key=lambda x:x[1].name):
        patch.variable = "enable_%s" % patch.name.replace("-","_").replace(".","_")
        lines.append("\t%s=\"$1\"\n" % patch.variable)
    lines.append("}\n")
    lines.append("\n")
    lines.append("# Enable or disable a specific patchset\n")
    lines.append("patch_enable ()\n")
    lines.append("{\n")
    lines.append("\tcase \"$1\" in\n")
    for i, patch in sorted([(i, all_patches[i]) for i in resolved], key=lambda x:x[1].name):
        lines.append("\t\t%s)\n" % patch.name)
        lines.append("\t\t\t%s=\"$2\"\n" % patch.variable)
        lines.append("\t\t\t;;\n")
    lines.append("\t\t*)\n")
    lines.append("\t\t\treturn 1\n")
    lines.append("\t\t\t;;\n")
    lines.append("\tesac\n")
    lines.append("\treturn 0\n")
    lines.append("}\n")
    lines_helpers = lines

    # Generate code for dependency resolver
    lines = []
    for i, patch in [(i, all_patches[i]) for i in reversed(resolved)]:
        if len(patch.depends):
            lines.append("if test \"$%s\" -eq 1; then\n" % patch.variable)
            for j in sorted(patch.depends):
                lines.append("\tif test \"$%s\" -gt 1; then\n" % all_patches[j].variable)
                lines.append("\t\tabort \"Patchset %s disabled, but %s depends on that.\"\n" %
                             (all_patches[j].name, patch.name))
                lines.append("\tfi\n")
            for j in sorted(patch.depends):
                lines.append("\t%s=1\n" % all_patches[j].variable)
            lines.append("fi\n\n")
    lines_resolver = lines

    # Generate code for applying all patchsets
    lines = []
    for i, patch in [(i, all_patches[i]) for i in resolved]:
        lines.append("# Patchset %s\n" % patch.name)
        lines.append("# |\n")

        # List all bugs fixed by this patchset
        if any([bugid is not None for bugid, bugname in patch.fixes]):
            lines.append("# | This patchset fixes the following Wine bugs:\n")
            for bugid, bugname in patch.fixes:
                if bugid is not None:
                    lines.append("# |   *\t%s\n" % "\n# | \t".join(textwrap.wrap("[#%d] %s" % (bugid, bugname), 120)))
            lines.append("# |\n")

        # List all modified files
        lines.append("# | Modified files:\n")
        lines.append("# |   *\t%s\n" % "\n# | \t".join(textwrap.wrap(", ".join(sorted(patch.modified_files)), 120)))
        lines.append("# |\n")
        lines.append("if test \"$%s\" -eq 1; then\n" % patch.variable)
        for f in patch.files:
            lines.append("\tpatch_apply %s\n" % os.path.join(patch.name, f))
        if len(patch.patches):
            lines.append("\t(\n")
            for p in _unique(patch.patches, key=lambda p: (p.patch_author, p.patch_subject, p.patch_revision)):
                lines.append("\t\techo '+    { \"%s\", \"%s\", %d },';\n" %
                             (_escape(p.patch_author), _escape(p.patch_subject), p.patch_revision))
            lines.append("\t) >> \"$patchlist\"\n")
        lines.append("fi\n\n")
    lines_apply = lines

    with open(config.path_template_script) as template_fp:
        template = template_fp.read()
    with open(config.path_script, "w") as fp:
        fp.write(template.format(patch_helpers="".join(lines_helpers).rstrip("\n"),
                                 patch_resolver="".join(lines_resolver).rstrip("\n"),
                                 patch_apply="".join(lines_apply).rstrip("\n")))

    # Add changes to git
    subprocess.call(["git", "add", config.path_script])

def generate_markdown(all_patches, stable_patches, stable_compholio_version):
    """Generate README.md including information about specific patches and bugfixes."""

    def _format_bug(mode, bugid, bugname):
        if mode < 0: bugname = "~~%s~~" % bugname
        if bugid is None: return "* %s" % bugname
        return "* %s ([Wine Bug #%d](https://bugs.winehq.org/show_bug.cgi?id=%d))" % \
               (bugname, bugid, bugid) #, short_desc.replace("\\", "\\\\").replace("\"", "\\\""))

    all_fixes  = {}

    # Get fixes for current version
    for _, patch in all_patches.iteritems():
        for bugid, bugname in patch.fixes:
            key = bugid if bugid is not None else bugname
            all_fixes[key] = [1, bugid, bugname]

    # Compare with fixes for latest stable version
    for _, patch in stable_patches.iteritems():
        for bugid, bugname in patch.fixes:
            key = bugid if bugid is not None else bugname
            if all_fixes.has_key(key):
                all_fixes[key][0] = 0
            else:
                all_fixes[key] = [-1, bugid, bugname]

    # Generate lists for all new and old fixes
    new_fixes = [(mode, bugid, bugname) for dummy, (mode, bugid, bugname) in
                                            all_fixes.iteritems() if mode > 0]
    old_fixes = [(mode, bugid, bugname) for dummy, (mode, bugid, bugname) in
                                            all_fixes.iteritems() if mode <= 0]

    # List of old fixes is not available when releasing a new version
    if len(old_fixes) == 0:
        old_fixes = new_fixes
        new_fixes = []

    # Generate information for current version
    lines = []
    if len(new_fixes):
        lines.append("**Bugfixes and features included in the next upcoming release [%d]:**" % len(new_fixes))
        lines.append("")
        for mode, bugid, bugname in sorted(new_fixes, key=lambda x: x[2]):
            lines.append(_format_bug(mode, bugid, bugname))
        lines.append("")
        lines.append("")
    lines.append("**Bugs fixed in Wine Staging %s [%d]:**" % (stable_compholio_version, len(old_fixes)))
    lines.append("")
    for mode, bugid, bugname in sorted(old_fixes, key=lambda x: x[2]):
        lines.append(_format_bug(mode, bugid, bugname))

    # Update README.md
    with open(config.path_template_README_md) as template_fp:
        template = template_fp.read()
    with open(config.path_README_md, "w") as fp:
        fp.write(template.format(fixes="\n".join(lines)))

    # Add changes to git
    subprocess.call(["git", "add", config.path_README_md])

if __name__ == "__main__":

    # Hack to avoid KeyboardInterrupts on different threads
    def _sig_int(signum=None, frame=None):
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        raise RuntimeError("CTRL+C pressed")
    signal.signal(signal.SIGINT, _sig_int)

    try:

        # Get information about Wine and Compholio version
        latest_wine_commit       = _latest_wine_commit(sys.argv[1] if len(sys.argv) >= 2 else None)
        stable_compholio_version = _stable_compholio_version()

        # Read current and stable patches
        all_patches    = read_patchset()
        stable_patches = read_patchset(revision="v%s" % stable_compholio_version)

        generate_ifdefined(all_patches)
        generate_script(all_patches)
        generate_markdown(all_patches, stable_patches, stable_compholio_version)

    except PatchUpdaterError as e:
        print ""
        print "ERROR: %s" % e
        print ""
        exit(1)
