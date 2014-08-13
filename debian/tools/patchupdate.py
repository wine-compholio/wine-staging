#!/usr/bin/python
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

from xml.dom import minidom
import contextlib
import hashlib
import itertools
import multiprocessing
import os
import patchutils
import pickle
import re
import subprocess
import sys
import textwrap
import urllib

# Cached information to speed up patch dependency checks
latest_wine_commit  = None
cached_patch_result = {}
cached_original_src = {}

class config(object):
    path_depcache           = ".depcache"
    path_srccache           = ".srccache"

    path_patches            = "patches"
    path_changelog          = "debian/changelog"
    path_wine               = "debian/tools/wine"

    path_template_Makefile  = "debian/tools/Makefile.in"
    path_Makefile           = "patches/Makefile"

    path_README_md          = "README.md"
    path_template_README_md = "debian/tools/README.md.in"

    path_DEVELOPER_md       = "DEVELOPER.md"
    path_template_DEVELOPER_md = "debian/tools/DEVELOPER.md.in"

class PatchUpdaterError(RuntimeError):
    """Failed to update patches."""
    pass

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

def _pairs(a):
    """Iterate over all pairs of elements contained in the list a."""
    for i, j in enumerate(a):
        for k in a[i+1:]:
            yield (j, k)

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

def _winebugs_query_short_desc(bugids):
    """Query short_desc from multiple wine bugzilla bugs at the same time."""
    bugids = list(set(bugids)) # Remove duplicates and convert to fixed order
    if len(bugids) == 0: return {}

    # Query bugzilla
    url = "http://bugs.winehq.org/show_bug.cgi?%s&ctype=xml&field=short_desc" % \
          "&".join(["id=%d" % bugid for bugid in bugids])
    with contextlib.closing(urllib.urlopen(url)) as fp:
        data = minidom.parseString(fp.read())

    # convert xml in a dictionary containing all bugs we found
    result = {}
    for element in data.getElementsByTagName('bug_id'):
        bugids.remove(int(element.firstChild.data))
    for bugid, element in zip(bugids, data.getElementsByTagName('short_desc')):
        result[bugid] = element.firstChild.data
    return result

# Read information from changelog
def _read_changelog():
    with open(config.path_changelog) as fp:
        for line in fp:
            r = re.match("^([a-zA-Z0-9][^(]*)\((.*)\) ([^;]*)", line)
            if r: yield (r.group(1).strip(), r.group(2).strip(), r.group(3).strip())

# Get version number of the latest stable release
def _stable_compholio_version():
    for package, version, distro in _read_changelog():
        if distro.lower() != "unreleased":
            return version

# Get latest wine commit
def _latest_wine_commit():
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
            with open(os.devnull, 'w') as devnull:
                content = subprocess.check_output(["git", "show", filename], stderr=devnull)
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
    """Read a definition file and return information as tuple (authors, depends, fixes)."""

    filename = os.path.join(filename, "definition")
    if revision is None:
        with open(filename) as fp:
            content = fp.read()
    else:
        filename = "%s:%s" % (revision, filename)
        try:
            with open(os.devnull, 'w') as devnull:
                content = subprocess.check_output(["git", "show", filename], stderr=devnull)
        except CalledProcessError:
            raise IOError("Failed to load %s" % filename)

    authors = []
    depends = set()
    fixes   = []
    info    = AuthorInfo()

    for line in content.split("\n"):
        if line.startswith("#"):
            continue

        tmp = line.split(":", 1)
        if len(tmp) != 2:
            if len(info.author) and len(info.subject):
                authors.append(info)
                info = AuthorInfo()
            continue

        key, val = tmp[0].lower(), tmp[1].strip()
        if key == "author":
            if len(info.author): info.author += ", "
            info.author += val

        elif key == "subject" or key == "title":
            if len(info.subject): info.subject += " "
            info.subject += val

        elif key == "revision":
            if len(info.revision): info.revision += ", "
            info.revision += val

        elif key == "depends":
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

        else:
            print "WARNING: Ignoring unknown command in definition file %s: %s" % (deffile, line)

    if len(info.author) and len(info.subject):
        authors.append(info)
    return authors, depends, fixes

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
            patch.authors, patch.depends, patch.fixes = \
                read_definition(revision, os.path.join(config.path_patches, patch.name), name_to_id)
        except IOError:
            raise PatchUpaterError("Missing definition file for %s" % patch.name)

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

def causal_time_permutations(all_patches, indices, filename):
    """Iterate over all possible permutations of patches affecting
       a specific file, which are compatible with dependencies."""
    for permutation in itertools.permutations(indices):
        if causal_time_relation(all_patches, permutation):
            selected_patches = []
            for i in permutation:
                selected_patches += [patch for patch in all_patches[i].patches if patch.modified_file == filename]
            yield selected_patches

def contains_binary_patch(all_patches, indices, filename):
    """Checks if any patch with given indices affecting filename is a binary patch."""
    for i in indices:
        for patch in all_patches[i].patches:
            if patch.modified_file == filename and patch.is_binary():
                return True
    return False

def get_wine_file(filename, force=False):
    """Return the hash and optionally the content of a file."""

    # If we're not forced, we try to save time and only lookup the cached checksum
    entry = "%s:%s" % (latest_wine_commit, filename)
    if not force and cached_original_src.has_key(entry):
        return (cached_original_src[entry], None)

    # Grab original file from the wine git repository
    try:
        with open(os.devnull, 'w') as devnull:
            content = subprocess.check_output(["git", "show", entry], cwd=config.path_wine, stderr=devnull)
    except subprocess.CalledProcessError as e:
        if e.returncode != 128: raise
        content = ""

    content_hash = hashlib.sha256(content).digest()
    cached_original_src[entry] = content_hash
    return (content_hash, content)

def verify_patch_order(all_patches, indices, filename):
    """Checks if the dependencies are defined correctly by applying on the patches on a copy from the git tree."""
    global cached_patch_result

    # If one of patches is a binary patch, then we cannot / won't verify it - require dependencies in this case
    if contains_binary_patch(all_patches, indices, filename):
        if not causal_time_relation_any(all_patches, indices):
            raise PatchUpdaterError("Because of binary patch modifying file %s the following patches need explicit dependencies: %s" %
                                    (filename, ", ".join([all_patches[i].name for i in indices])))
        return

    # Get at least the checksum of the original file
    original_content_hash, original_content = get_wine_file(filename)

    # Check for possible ways to apply the patch
    failed_to_apply   = False
    last_result_hash  = None
    for patches in causal_time_permutations(all_patches, indices, filename):

        # Calculate unique hash based on the original content and the order in which the patches are applied
        m = hashlib.sha256()
        m.update(original_content_hash)
        for patch in patches:
            m.update(patch.hash())
        unique_hash = m.digest()

        # Fast path -> we know that it applies properly
        if cached_patch_result.has_key(unique_hash):
            result_hash = cached_patch_result[unique_hash]

        else:
            # Now really get the file, if we don't have it yet
            if original_content is None:
                original_content_hash, original_content = get_wine_file(filename, force=True)

            # Apply the patches (without fuzz)
            try:
                content = patchutils.apply_patch(original_content, patches, fuzz=0)
            except patchutils.PatchApplyError:
                if last_result_hash is not None: break
                failed_to_apply = True
                continue

            # Get hash of resulting file and add to cache
            result_hash = hashlib.sha256(content).digest()
            cached_patch_result[unique_hash] = result_hash

        if last_result_hash is None:
            last_result_hash = result_hash
            if failed_to_apply: break
        elif last_result_hash != result_hash:
            last_result_hash = None
            break

    # If something failed, then show the appropriate error message.
    if failed_to_apply and last_result_hash is None:
        raise PatchUpdaterError("Changes to file %s don't apply on git source tree: %s" %
                                (filename, ", ".join([all_patches[i].name for i in indices])))

    elif failed_to_apply or last_result_hash is None:
        raise PatchUpdaterError("Depending on the order some changes to file %s dont't apply / lead to different results: %s" %
                                (filename, ", ".join([all_patches[i].name for i in indices])))

    else:
        assert len(last_result_hash) == 32

def verify_dependencies(all_patches):
    """Resolve dependencies, and afterwards run verify_patch_order() to check if everything applies properly."""

    def _load_patch_cache():
        """Load dictionary for cached patch dependency tests into cached_patch_result."""
        global cached_patch_result
        global cached_original_src
        cached_patch_result = _load_dict(config.path_depcache)
        cached_original_src = _load_dict(config.path_srccache)

    def _save_patch_cache():
        """Save dictionary for cached patch depdency tests."""
        _save_dict(config.path_depcache, cached_patch_result)
        _save_dict(config.path_srccache, cached_original_src)

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
            raise PatchUpdaterError("Circular dependency in set of patches: %s" %
                                    ", ".join([patch.name for i, patch in patches.iteritems()]))

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

    # Check if patches always apply correctly
    _load_patch_cache()
    try:
        for f, indices in modified_files.iteritems():
            verify_patch_order(all_patches, indices, f)
    finally:
        _save_patch_cache()

def generate_makefile(all_patches):
    """Generate Makefile for a specific set of patches."""

    with open(config.path_template_Makefile) as template_fp:
        template = template_fp.read()

    with open(config.path_Makefile, "w") as fp:
        fp.write(template.format(patchlist="\t" + " \\\n\t".join(["%s.ok" % patch.name for i, patch in all_patches.iteritems()])))

        for i, patch in all_patches.iteritems():
            fp.write("# Patchset %s\n" % patch.name)
            fp.write("# |\n")
            fp.write("# | Included patches:\n")

            # List all patches and their corresponding authors
            for info in patch.authors:
                if not info.subject: continue
                s = []
                if info.revision and info.revision != "1": s.append("rev %s" % info.revision)
                if info.author: s.append("by %s" % info.author)
                if len(s): s = " [%s]" % ", ".join(s)
                fp.write("# |   *\t%s\n" % "\n# | \t".join(textwrap.wrap(info.subject + s, 120)))
            fp.write("# |\n")

            # List all bugs fixed by this patchset
            if any([bugid is not None for bugid, bugname in patch.fixes]):
                fp.write("# | This patchset fixes the following Wine bugs:\n")
                for bugid, bugname in patch.fixes:
                    if bugid is not None:
                        fp.write("# |   *\t%s\n" % "\n# | \t".join(textwrap.wrap("[#%d] %s" % (bugid, bugname), 120)))
                fp.write("# |\n")

            # List all modified files
            fp.write("# | Modified files: \n")
            fp.write("# |   *\t%s\n" % "\n# | \t".join(textwrap.wrap(", ".join(sorted(patch.modified_files)), 120)))
            fp.write("# |\n")

            # Generate dependencies and code to apply patches
            fp.write(".INTERMEDIATE: %s.ok\n" % patch.name)
            depends = " ".join([""] + ["%s.ok" % all_patches[d].name for d in patch.depends]) if len(patch.depends) else ""
            fp.write("%s.ok:%s\n" % (patch.name, depends))
            for f in patch.files:
                fp.write("\t$(call APPLY_FILE,%s)\n" % os.path.join(patch.name, f))

            # Create *.ok file (used to generate patchlist)
            if len(patch.authors):
                fp.write("\t@( \\\n")
                for info in patch.authors:
                    if not info.subject: continue
                    s = info.subject.replace("\\", "\\\\\\\\").replace("\"", "\\\\\"")
                    if info.revision and info.revision != "1": s += " [rev %s]" % info.revision
                    fp.write("\t\techo '+    { \"%s\", \"%s\", \"%s\" },'; \\\n" % (patch.name, info.author, s))
                fp.write("\t) > %s.ok\n" % patch.name)
            else:
                fp.write("\ttouch %s.ok\n" % patch.name)
            fp.write("\n");

def generate_markdown(all_patches, stable_patches, stable_compholio_version):
    """Generate README.md and DEVELOPER.md including information about specific patches and bugfixes."""

    def _format_bug(mode, bugid, bugname):
        if bugid is not None:
            short_desc = bug_short_desc[bugid]
            if bugname is None: bugname = short_desc
        if mode < 0: bugname = "~~%s~~" % bugname
        if bugid is None: return "* %s" % bugname
        return "* %s ([Wine Bug #%d](http://bugs.winehq.org/show_bug.cgi?id=%d \"%s\"))" % \
               (bugname, bugid, bugid, short_desc.replace("\\", "\\\\").replace("\"", "\\\""))

    all_bugids = set()
    all_fixes  = {}

    # Get fixes for current version
    for i, patch in all_patches.iteritems():
        for bugid, bugname in patch.fixes:
            if bugid is not None: all_bugids.add(bugid)
            key = bugid if bugid is not None else bugname
            all_fixes[key] = [1, bugid, bugname]

    # Compare with fixes for latest stable version
    for i, patch in stable_patches.iteritems():
        for bugid, bugname in patch.fixes:
            if bugid is not None: all_bugids.add(bugid)
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

    # Query information from bugzilla
    bug_short_desc = _winebugs_query_short_desc(all_bugids)

    # Generate information for current version
    lines = []
    if len(new_fixes):
        lines.append("**Bugfixes and features included in the next upcoming release [%d]:**" % len(new_fixes))
        lines.append("")
        for mode, bugid, bugname in sorted(new_fixes, key=lambda x: x[2]):
            lines.append(_format_bug(mode, bugid, bugname))
        lines.append("")
        lines.append("")
    lines.append("**Bugs fixed in Wine-Compholio %s [%d]:**" % (stable_compholio_version, len(old_fixes)))
    lines.append("")
    for mode, bugid, bugname in sorted(old_fixes, key=lambda x: x[2]):
        lines.append(_format_bug(mode, bugid, bugname))

    # Update README.md
    with open(config.path_template_README_md) as template_fp:
        template = template_fp.read()
    with open(config.path_README_md, "w") as fp:
        fp.write(template.format(fixes="\n".join(lines)))

    # Update DEVELOPER.md
    with open(config.path_template_DEVELOPER_md) as template_fp:
        template = template_fp.read()
    with open(config.path_DEVELOPER_md, "w") as fp:
        fp.write(template.format(version=stable_compholio_version))

if __name__ == "__main__":
    try:

        # Get information about Wine and Compholio version
        latest_wine_commit       = _latest_wine_commit()
        stable_compholio_version = _stable_compholio_version()

        # Read current and stable patches
        all_patches    = read_patchset()
        stable_patches = read_patchset(revision="v%s" % stable_compholio_version)

        # Check dependencies
        verify_dependencies(all_patches)

        # Update Makefile, README.md and DEVELOPER.md
        generate_makefile(all_patches)
        generate_markdown(all_patches, stable_patches, stable_compholio_version)

    except PatchUpdaterError as e:
        print ""
        print "ERROR: %s" % e
        print ""
        exit(1)
