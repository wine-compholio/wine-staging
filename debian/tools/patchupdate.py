#!/usr/bin/python2
#
# Automatic patch dependency checker and Makefile/README.md generator.
#
# Copyright (C) 2014 Sebastian Lackner
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
    path_depcache           = ".patchupdate.cache"

    path_patches            = "patches"
    path_changelog          = "debian/changelog"
    path_wine               = "debian/tools/wine"

    path_template_Makefile  = "debian/tools/Makefile.in"
    path_Makefile           = "patches/Makefile"

    path_README_md          = "README.md"
    path_template_README_md = "debian/tools/README.md.in"

class PatchUpdaterError(RuntimeError):
    """Failed to update patches."""
    pass

class PatchSet(object):
    def __init__(self, name):
        self.name           = name
        self.fixes          = []
        self.changes        = []
        self.disabled       = False

        self.files          = []
        self.patches        = []
        self.modified_files = set()
        self.depends        = set()

        self.verify_depends = set()
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

def _merge_seq(iterable, callback=None):
    """Merge lists/iterators into a new one. Call callback after each chunk"""
    for i, items in enumerate(iterable):
        if callback is not None:
            callback(i)
        for obj in items:
            yield obj

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

def _latest_wine_commit():
    """Get latest wine commit."""
    if not os.path.isdir(config.path_wine):
        raise PatchUpdaterError("Please create a symlink to the wine repository in %s" % config.path_wine)
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
            subdirectory = os.path.join(path, name)
            if not os.path.isdir(subdirectory):
                continue
            dirs.append((name, subdirectory))
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

def read_definition(revision, filename, name_to_id):
    """Read a definition file and return information as tuple (depends, fixes)."""
    filename = os.path.join(filename, "definition")
    if revision is None:
        with open(filename) as fp:
            content = fp.read()
    else:
        filename = "%s:%s" % (revision, filename)
        try:
            content = subprocess.check_output(["git", "show", filename], stderr=_devnull)
        except subprocess.CalledProcessError:
            raise IOError("Failed to load %s" % filename)

    depends  = set()
    fixes    = []
    disabled = False

    for line in content.split("\n"):
        if line.startswith("#"):
            continue
        tmp = line.split(":", 1)
        if len(tmp) != 2:
            continue
        key, val = tmp[0].lower(), tmp[1].strip()
        if key == "depends":
            if name_to_id is not None:
                if not name_to_id.has_key(val):
                    raise PatchUpdaterError("Definition file %s references unknown dependency %s" % (filename, val))
                depends.add(name_to_id[val])
        elif key == "fixes":
            r = re.match("^[0-9]+$", val)
            if r:
                fixes.append((int(val), None))
                continue
            r = re.match("^\\[ *([0-9]+) *\\](.*)$", val)
            if r:
                fixes.append((int(r.group(1)), r.group(2).strip()))
                continue
            fixes.append((None, val))
        elif key == "disabled":
            disabled = _parse_int(val)
        elif revision is None:
            print "WARNING: Ignoring unknown command in definition file %s: %s" % (filename, line)

    return depends, fixes, disabled

def read_patchset(revision = None):
    """Read information about all patchsets for a specific revision."""
    unique_id   = itertools.count()
    all_patches = {}
    name_to_id  = {}

    # Read in sorted order (to ensure created Makefile doesn't change too much)
    for name, subdirectory in sorted(enum_directories(revision, config.path_patches)):
        patch = PatchSet(name)

        if revision is None:

            # If its the latest revision, then request additional information
            if not os.path.isdir(subdirectory):
                raise RuntimeError("Unable to open directory %s" % subdirectory)

            # Enumerate .patch files in the given directory, enumerate individual patches and affected files
            for f in sorted(os.listdir(subdirectory)):
                if not f.endswith(".patch") or not os.path.isfile(os.path.join(subdirectory, f)):
                    continue
                patch.files.append(f)
                for p in patchutils.read_patch(os.path.join(subdirectory, f)):
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
            patch.depends, patch.fixes, patch.disabled = \
                read_definition(revision, os.path.join(config.path_patches, patch.name), name_to_id)
        except IOError:
            patch.depends, patch.fixes, patch.disabled = set(), [], False

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

def causal_time_permutations(all_patches, indices):
    """Iterate over all possible permutations of patches affecting
       a specific file, which are compatible with dependencies."""
    for permutation in itertools.permutations(indices):
        if causal_time_relation(all_patches, permutation):
            yield permutation

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

def select_patches(all_patches, indices, filename):
    """Create a temporary patch file for each patchset and calculate the checksum."""
    selected_patches = {}

    for i in indices:
        p = tempfile.NamedTemporaryFile()
        m = hashlib.sha256()

        for patch in all_patches[i].patches:
            if patch.modified_file != filename:
                continue
            for chunk in patch.read_chunks():
                p.write(chunk)
                m.update(chunk)
            p.write("\n")
            m.update("\n")

        p.flush()
        selected_patches[i]  = (m.digest(), p)

    return selected_patches

def verify_patch_order(all_patches, indices, filename, pool):
    """Checks if the dependencies are defined correctly by applying
       the patches on a (temporary) copy from the git tree."""

    # If one of patches is a binary patch, then we cannot / won't verify it - require dependencies in this case
    if contains_binary_patch(all_patches, indices, filename):
        if not causal_time_relation_any(all_patches, indices):
            raise PatchUpdaterError("Because of binary patch modifying file %s the following patches need explicit dependencies: %s" %
                                    (filename, ", ".join([all_patches[i].name for i in indices])))
        return

    original_content      = get_wine_file(filename)
    original_content_hash = _sha256(original_content)
    selected_patches      = select_patches(all_patches, indices, filename)
    try:

        def _test_apply(permutations):
            """Tests if specific permutations of patches apply on the wine source tree."""
            patch_stack_indices = []
            patch_stack_patches = []
            try:

                for permutation in permutations:

                    # Calculate hash
                    m = hashlib.sha256()
                    m.update(original_content_hash)
                    for i in permutation:
                        m.update(selected_patches[i][0])
                    input_hash = m.digest()

                    # Fast path -> we know that it applies properly
                    try:
                        yield cached_patch_result[input_hash]
                        continue

                    except KeyError:
                        pass

                    # Remove unneeded patches from patch stack
                    while list(permutation[:len(patch_stack_indices)]) != patch_stack_indices:
                        patch_stack_indices.pop()
                        patch_stack_patches.pop().close()

                    # Apply the patches (without fuzz)
                    try:
                        while len(patch_stack_indices) < len(permutation):
                            i = permutation[len(patch_stack_indices)]
                            original  = patch_stack_patches[-1] if len(patch_stack_indices) else original_content
                            patchfile = selected_patches[i][1]
                            patch_stack_patches.append(patchutils.apply_patch(original, patchfile, fuzz=0))
                            patch_stack_indices.append(i)
                        output_hash = _sha256(patch_stack_patches[-1])

                    except patchutils.PatchApplyError:
                        output_hash = None

                    cached_patch_result[input_hash] = output_hash
                    yield output_hash

            finally:
                # Ensure temporary files are cleaned up properly
                while len(patch_stack_patches):
                    patch_stack_patches.pop().close()

        # Show a progress bar while applying the patches - this task might take some time
        chunk_size  = 20
        total_tasks = (math.factorial(len(indices)) + chunk_size - 1) / chunk_size
        with progressbar.ProgressBar(desc=filename, total=total_tasks) as progress:

            failed_to_apply   = False
            last_result_hash  = None

            # Check for possible ways to apply the patch
            it = _split_seq(causal_time_permutations(all_patches, indices), chunk_size)
            for output_hash in _merge_seq(pool.imap_unordered(lambda seq: list(_test_apply(seq)), it), \
                                          callback=progress.update):

                # Failed to apply patch, continue checking the rest.
                if output_hash is None:
                    failed_to_apply = True
                    if last_result_hash is None:
                        continue
                    break

                # No known hash yet, remember the result. If we failed applying before, we can stop now.
                elif last_result_hash is None:
                    last_result_hash = output_hash
                    if failed_to_apply: break

                # Applied successful, but result has a different hash - also treat as failure.
                elif last_result_hash != output_hash:
                    failed_to_apply = True
                    break

            if failed_to_apply:
                progress.finish("<failed to apply>")
            elif verbose:
                progress.finish(binascii.hexlify(last_result_hash))

    finally:
        original_content.close()
        for _, (_, p) in selected_patches.iteritems():
            p.close()

    # If something failed, then show the appropriate error message.
    if failed_to_apply and last_result_hash is None:
        raise PatchUpdaterError("Changes to file %s don't apply on git source tree: %s" %
                                (filename, ", ".join([all_patches[i].name for i in indices])))

    elif failed_to_apply:
        raise PatchUpdaterError("Depending on the order some changes to file %s don't apply / lead to different results: %s" %
                                (filename, ", ".join([all_patches[i].name for i in indices])))

    else:
        assert len(last_result_hash) == 32

def verify_dependencies(all_patches):
    """Resolve dependencies, and afterwards run verify_patch_order() to check if everything applies properly."""

    def _load_patch_cache():
        """Load dictionary for cached patch dependency tests."""
        global cached_patch_result
        cached_patch_result = _load_dict(config.path_depcache)

    def _save_patch_cache():
        """Save dictionary for cached patch dependency tests."""
        _save_dict(config.path_depcache, cached_patch_result.copy())

    enabled_patches = dict([(i, patch) for i, patch in all_patches.iteritems() if not patch.disabled])
    max_patches     = max(enabled_patches.keys()) + 1

    for i, patch in enabled_patches.iteritems():
        patch.verify_depends = set(patch.depends)
        patch.verify_time    = [0]*max_patches

    # Check for circular dependencies and perform modified vector clock algorithm
    patches = dict(enabled_patches)
    while len(patches):

        to_delete = []
        for i, patch in patches.iteritems():
            if len(patch.verify_depends) == 0:
                patch.verify_time[i] += 1
                to_delete.append(i)

        if len(to_delete) == 0:
            raise PatchUpdaterError("Circular dependency (or disabled dependency) in set of patches: %s" %
                                    ", ".join([patch.name for i, patch in patches.iteritems()]))

        for j in to_delete:
            for i, patch in patches.iteritems():
                if i != j and j in patch.verify_depends:
                    patch.verify_time = causal_time_combine(patch.verify_time, patches[j].verify_time)
                    patch.verify_depends.remove(j)
            del patches[j]

    # Find out which files are modified by multiple patches
    modified_files = {}
    for i, patch in enabled_patches.iteritems():
        for f in patch.modified_files:
            if f not in modified_files:
                modified_files[f] = []
            modified_files[f].append(i)

    # Check if patches always apply correctly
    _load_patch_cache()
    pool = multiprocessing.pool.ThreadPool(processes=8)
    try:
        for f, indices in modified_files.iteritems():
            verify_patch_order(enabled_patches, indices, f, pool)
    finally:
        _save_patch_cache()
        pool.close()

def generate_makefile(all_patches):
    """Generate Makefile for a specific set of patches."""

    with open(config.path_template_Makefile) as template_fp:
        template = template_fp.read()

    with open(config.path_Makefile, "w") as fp:
        fp.write(template.format(patchlist="\t" + " \\\n\t".join(
            ["%s.ok" % patch.name for _, patch in all_patches.iteritems() if not patch.disabled])))

        for _, patch in all_patches.iteritems():
            fp.write("# Patchset %s\n" % patch.name)
            fp.write("# |\n")

            # List all bugs fixed by this patchset
            if any([bugid is not None for bugid, bugname in patch.fixes]):
                fp.write("# | This patchset fixes the following Wine bugs:\n")
                for bugid, bugname in patch.fixes:
                    if bugid is not None:
                        fp.write("# |   *\t%s\n" % "\n# | \t".join(textwrap.wrap("[#%d] %s" % (bugid, bugname), 120)))
                fp.write("# |\n")

            # List all modified files
            fp.write("# | Modified files:\n")
            fp.write("# |   *\t%s\n" % "\n# | \t".join(textwrap.wrap(", ".join(sorted(patch.modified_files)), 120)))
            fp.write("# |\n")

            # Generate dependencies and code to apply patches
            fp.write(".INTERMEDIATE: %s.ok\n" % patch.name)
            depends = " ".join([""] + ["%s.ok" % all_patches[d].name for d in patch.depends]) if len(patch.depends) else ""
            fp.write("%s.ok:%s\n" % (patch.name, depends))
            for f in patch.files:
                fp.write("\t$(call APPLY_FILE,%s)\n" % os.path.join(patch.name, f))

            # Create *.ok file (used to generate patchlist)
            if len(patch.patches):
                fp.write("\t@( \\\n")
                for p in _unique(patch.patches, key=lambda p: (p.patch_author, p.patch_subject, p.patch_revision)):
                    fp.write("\t\techo '+    { \"%s\", \"%s\", %d },'; \\\n" % \
                            (_escape(p.patch_author), _escape(p.patch_subject), p.patch_revision))
                fp.write("\t) > %s.ok\n" % patch.name)
            else:
                fp.write("\ttouch %s.ok\n" % patch.name)
            fp.write("\n");

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

if __name__ == "__main__":
    verbose = "-v" in sys.argv[1:]

    # Hack to avoid KeyboardInterrupts on worker threads
    def _sig_int(signum=None, frame=None):
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        raise RuntimeError("CTRL+C pressed")
    signal.signal(signal.SIGINT, _sig_int)

    try:

        # Get information about Wine and Compholio version
        latest_wine_commit       = _latest_wine_commit()
        stable_compholio_version = _stable_compholio_version()

        # Read current and stable patches
        all_patches    = read_patchset()
        stable_patches = read_patchset(revision="v%s" % stable_compholio_version)

        # Check dependencies
        verify_dependencies(all_patches)

        # Update Makefile and README.md
        generate_makefile(all_patches)
        generate_markdown(all_patches, stable_patches, stable_compholio_version)

    except PatchUpdaterError as e:
        print ""
        print "ERROR: %s" % e
        print ""
        exit(1)
