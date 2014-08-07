#!/usr/bin/python
#
# Python functions to read, split and apply patches.
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

import collections
import difflib
import hashlib
import itertools
import os
import re
import subprocess
import tempfile

class PatchParserError(RuntimeError):
    """Unable to parse patch file - either an unimplemented feature, or corrupted patch."""
    pass

class PatchApplyError(RuntimeError):
    """Failed to apply/merge patch."""
    pass

class PatchObject(object):
    def __init__(self, filename):
        self.extracted_patch        = None
        self.unique_hash            = None

        self.filename               = filename
        self.offset_begin           = None
        self.offset_end             = None
        self.isbinary               = False

        self.oldname                = None
        self.newname                = None
        self.modified_file          = None

        self.oldsha1                = None
        self.newsha1                = None
        self.newmode                = None

    def is_binary(self):
        return self.isbinary

    def read_chunks(self):
        """Iterates over arbitrary sized chunks of this patch."""
        assert self.offset_end >= self.offset_begin
        with open(self.filename) as fp:
            fp.seek(self.offset_begin)
            i = self.offset_end - self.offset_begin
            while i > 0:
                buf = fp.read(4096 if i > 4096 else i)
                if buf == "": raise IOError("Unable to extract patch.")
                yield buf
                i -= len(buf)

    def extract(self):
        """Create a temporary file containing the extracted patch."""
        if not self.extracted_patch:
            self.extracted_patch = tempfile.NamedTemporaryFile()
            for chunk in self.read_chunks():
                self.extracted_patch.write(chunk)
            self.extracted_patch.flush()
        return self.extracted_patch

    def hash(self):
        """Hash the content of the patch."""
        if not self.unique_hash:
            m = hashlib.sha256()
            for chunk in self.read_chunks():
                m.update(chunk)
            self.unique_hash = m.digest()
        return self.unique_hash

def read_patch(filename):
    """Iterates over all patches contained in a file, and returns PatchObject objects."""

    class _FileReader(object):
        def __init__(self, filename):
            self.filename = filename
            self.fp       = open(self.filename)
            self.peeked   = None

        def close(self):
            self.fp.close()

        def __enter__(self):
            return self

        def __exit__(self, type, value, traceback):
            self.close()

        def seek(self, pos):
            """Change the file cursor position."""
            self.fp.seek(pos)
            self.peeked = None

        def tell(self):
            """Return the current file cursor position."""
            if self.peeked is None:
                return self.fp.tell()
            return self.peeked[0]

        def peek(self):
            """Read one line without changing the file cursor."""
            if self.peeked is None:
                pos = self.fp.tell()
                tmp = self.fp.readline()
                if len(tmp) == 0: return None
                self.peeked = (pos, tmp)
            return self.peeked[1]

        def read(self):
            """Read one line from the file, and move the file cursor to the next line."""
            if self.peeked is None:
                tmp = self.fp.readline()
                if len(tmp) == 0: return None
                return tmp
            tmp, self.peeked = self.peeked, None
            return tmp[1]

    def _read_single_patch(fp, oldname=None, newname=None):
        """Internal function to read a single patch from a file."""

        patch = PatchObject(fp.filename)
        patch.offset_begin = fp.tell()
        patch.oldname = oldname
        patch.newname = newname

        # Skip over initial diff --git header
        line = fp.peek()
        if line.startswith("diff --git "):
            assert fp.read() == line

        # Read header
        while True:
            line = fp.peek()
            if line is None:
                break
            elif line.startswith("--- "):
                patch.oldname = line[4:].strip()
            elif line.startswith("+++ "):
                patch.newname = line[4:].strip()
            elif line.startswith("old mode") or line.startswith("deleted file mode"):
                pass # ignore
            elif line.startswith("new mode "):
                patch.newmode = line[9:].strip()
            elif line.startswith("new file mode "):
                patch.newmode = line[14:].strip()
            elif line.startswith("new mode") or line.startswith("new file mode"):
                raise PatchParserError("Unable to parse header line '%s'." % line)
            elif line.startswith("copy from") or line.startswith("copy to"):
                raise NotImplementedError("Patch copy header not implemented yet.")
            elif line.startswith("rename "):
                raise NotImplementedError("Patch rename header not implemented yet.")
            elif line.startswith("similarity index") or line.startswith("dissimilarity index"):
                pass # ignore
            elif line.startswith("index "):
                r = re.match("^index ([a-fA-F0-9]*)\.\.([a-fA-F0-9]*)", line)
                if not r: raise PatchParserError("Unable to parse index header line '%s'." % line)
                patch.oldsha1, patch.newsha1 = r.group(1), r.group(2)
            else:
                break
            assert fp.read() == line

        if patch.oldname is None or patch.newname is None:
            raise PatchParserError("Missing old or new name.")
        elif patch.oldname == "/dev/null" and patch.newname == "/dev/null":
            raise PatchParserError("Old and new name is /dev/null?")

        if patch.oldname.startswith("a/"):
            patch.oldname = patch.oldname[2:]
        elif patch.oldname != "/dev/null":
            raise PatchParserError("Old name in patch doesn't start with a/.")

        if patch.newname.startswith("b/"):
            patch.newname = patch.newname[2:]
        elif patch.newname != "/dev/null":
            raise PatchParserError("New name in patch doesn't start with b/.")

        if patch.newname != "/dev/null":
            patch.modified_file = patch.newname
        else:
            patch.modified_file = patch.oldname

        # Decide between binary and textual patch
        if line is None or line.startswith("diff --git ") or line.startswith("--- "):
            if oldname != newname:
                raise PatchParserError("Stripped old- and new name doesn't match.")

        elif line.startswith("@@ -"):
            while True:
                line = fp.peek()
                if line is None or not line.startswith("@@ -"):
                    break

                r = re.match("^@@ -(([0-9]+),)?([0-9]+) \+(([0-9]+),)?([0-9]+) @@", line)
                if not r: raise PatchParserError("Unable to parse hunk header '%s'." % line)
                srcpos = max(int(r.group(2)) - 1, 0) if r.group(2) else 0
                dstpos = max(int(r.group(5)) - 1, 0) if r.group(5) else 0
                srclines, dstlines = int(r.group(3)), int(r.group(6))
                if srclines <= 0 and dstlines <= 0:
                    raise PatchParserError("Empty hunk doesn't make sense.")
                assert fp.read() == line

                while srclines > 0 or dstlines > 0:
                    line = fp.read()
                    if line is None:
                        raise PatchParserError("Truncated patch.")
                    elif line.startswith(" "):
                        if srclines == 0 or dstlines == 0:
                            raise PatchParserError("Corrupted patch.")
                        srclines -= 1
                        dstlines -= 1
                    elif line.startswith("-"):
                        if srclines == 0:
                            raise PatchParserError("Corrupted patch.")
                        srclines -= 1
                    elif line.startswith("+"):
                        if dstlines == 0:
                            raise PatchParserError("Corrupted patch.")
                        dstlines -= 1
                    elif line.startswith("\\ "):
                        pass # ignore
                    else:
                        raise PatchParserError("Unexpected line in hunk.")

                while True:
                    line = fp.peek()
                    if line is None or not line.startswith("\\ "): break
                    assert fp.read() == line

        elif line.rstrip() == "GIT binary patch":
            if patch.oldsha1 is None or patch.newsha1 is None:
                raise PatchParserError("Missing index header, sha1 sums required for binary patch.")
            elif patch.oldname != patch.newname:
                raise PatchParserError("Stripped old- and new name doesn't match for binary patch.")
            assert fp.read() == line

            line = fp.read()
            if line is None: raise PatchParserError("Unexpected end of file.")
            r = re.match("^(literal|delta) ([0-9]+)", line)
            if not r: raise NotImplementedError("Only literal/delta patches are supported.")
            patch.isbinary = True

            # Skip over patch data
            while True:
                line = fp.read()
                if line is None or line.strip() == "":
                    break

        else:
            raise PatchParserError("Unknown patch format.")

        patch.offset_end = fp.tell()
        return patch

    with _FileReader(filename) as fp:
        while True:
            line = fp.peek()
            if line is None:
                break
            elif line.startswith("diff --git "):
                tmp = line.strip().split(" ")
                if len(tmp) != 4: raise PatchParserError("Unable to parse git diff header line '%s'." % line)
                yield _read_single_patch(fp, tmp[2].strip(), tmp[3].strip())
            elif line.startswith("--- "):
                yield _read_single_patch(fp)
            elif line.startswith("@@ -") or line.startswith("+++ "):
                raise PatchParserError("Patch didn't start with a git or diff header.")
            else:
                assert fp.read() == line

def apply_patch(content, patches, reverse=False, fuzz=2):
    """Apply a patch with optional fuzz - uses the commandline 'patch' utility."""

    if not isinstance(patches, collections.Sequence):
        patches = [patches]

    contentfile = tempfile.NamedTemporaryFile(delete=False)
    try:
        contentfile.write(content)
        contentfile.close()

        for patch in patches:

            patchfile = patch.extract()
            cmdline = ["patch", "--force", "--silent", "-r", "-"]
            if reverse:   cmdline.append("--reverse")
            if fuzz != 2: cmdline.append("--fuzz=%d" % fuzz)
            cmdline += [contentfile.name, patchfile.name]

            with open(os.devnull, 'w') as devnull:
                exitcode = subprocess.call(cmdline, stdout=devnull, stderr=devnull)
            if exitcode != 0:
                raise PatchApplyError("Failed to apply patch (exitcode %d)." % exitcode)

        with open(contentfile.name) as fp:
            content = fp.read()

    finally:
        os.unlink(contentfile.name)

    return content

