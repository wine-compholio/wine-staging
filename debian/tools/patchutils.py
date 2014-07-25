import re
import os
import tempfile
import itertools
import difflib
import subprocess
import hashlib

class GeneralPatchError(RuntimeError):
    pass

class PatchParserError(GeneralPatchError):
    """Unable to parse patch file - either an unimplemented feature, or corrupted patch."""
    pass

class PatchApplyError(GeneralPatchError):
    """Failed to apply/merge patch."""
    pass

class Patch(object):
    def __init__(self):
        self.extracted_patch = None

    def is_empty(self):
        raise NotImplementedError("is_empty not implemented.")

    def min_source_size(self):
        raise NotImplementedError("min_source_size not implemented.")

    def min_dest_size(self):
        raise NotImplementedError("min_dest_size not implemented.")

    def read_chunks(self):
        raise NotImplementedError("read_chunks not implemented.")

    def read_hunks(self, reverse=False):
        raise NotImplementedError("read_hunks not implemented.")

    def extract(self):
        """Create a temporary file containing the extracted patch."""
        if not self.extracted_patch:
            self.extracted_patch = tempfile.NamedTemporaryFile()
            for chunk in self.read_chunks():
                self.extracted_patch.write(chunk)
            self.extracted_patch.flush()
        return self.extracted_patch

    def hash(self):
        m = hashlib.md5()
        for srcpos, srchunk, dsthunk in self.read_hunks():
            m.update(hashlib.md5("\n".join(srchunk)).digest())
            m.update(hashlib.md5("\n".join(dsthunk)).digest())
        return m.digest()

class FilePatch(Patch):
    def __init__(self, filename):
        super(FilePatch, self).__init__()

        self.filename               = filename
        self.offset_begin           = None
        self.offset_end             = None

        self.oldname                = None
        self.newname                = None
        self.modified_file          = None

        self.oldsha1                = None
        self.newsha1                = None
        self.newmode                = None

        self.hunks                  = [] # offset, srcpos, srclines, dstpos, dstlines

        self.isbinary               = False
        self.binary_patch_offset    = None
        self.binary_patch_type      = None
        self.binary_patch_size      = None

    def is_empty(self):
        return len(self.hunks) == 0

    def min_source_size(self):
        """Returns the minimum size of the source file, so that the patch can apply."""
        if self.isbinary:
            raise GeneralPatchError("Not possible to calculate minimum source size for binary patches.")
        elif len(self.hunks) == 0:
            return 0
        last = max(self.hunks, key=lambda x: x[1]+x[2])
        return last[1]+last[2]

    def min_dest_size(self):
        """Returns the minimum size of the destination file, so that the patch can apply."""
        if self.isbinary:
            raise GeneralPatchError("Not possible to calculate minimum destination size for binary patches.")
        elif len(self.hunks) == 0:
            return 0
        last = max(self.hunks, key=lambda x: x[3]+x[4])
        return last[3]+last[4]

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

    def read_hunks(self, reverse=False):
        """Iterates over hunks contained in this patch, reverse exchanges source and destination."""
        if self.isbinary:
            raise GeneralPatchError("Command not allowed for binary patches.")

        with open(self.filename) as fp:
            for offset, srcpos, srclines, dstpos, dstlines in self.hunks:
                fp.seek(offset)

                srchunk = []
                dsthunk = []

                while srclines > 0 or dstlines > 0:
                    line = fp.readline()
                    if line == "":
                        raise PatchParserError("Truncated patch.")
                    line = line.rstrip("\r\n")
                    if line.startswith(" "):
                        if srclines == 0 or dstlines == 0:
                            raise PatchParserError("Corrupted patch.")
                        srchunk.append(line[1:])
                        dsthunk.append(line[1:])
                        srclines -= 1
                        dstlines -= 1
                    elif line.startswith("-"):
                        if srclines == 0:
                            raise PatchParserError("Corrupted patch.")
                        srchunk.append(line[1:])
                        srclines -= 1
                    elif line.startswith("+"):
                        if dstlines == 0:
                            raise PatchParserError("Corrupted patch.")
                        dsthunk.append(line[1:])
                        dstlines -= 1
                    elif line.startswith("\\ "):
                        pass # ignore
                    else:
                        raise PatchParserError("Unexpected line in hunk.")

                if reverse:
                    yield dstpos, dsthunk, srchunk
                else:
                    yield srcpos, srchunk, dsthunk

class MemoryPatch(Patch):
    def __init__(self):
        super(MemoryPatch, self).__init__()

        self.oldname = None
        self.newname = None
        self.modified_file = None

        self.hunks = [] # srcpos, srclines, dstpos, dstlines, lines

    def is_empty(self):
        return len(self.hunks) == 0

    def min_source_size(self):
        """Returns the minimum size of the source file, so that the patch can apply."""
        if len(self.hunks) == 0:
            return 0
        last = max(self.hunks, key=lambda x: x[0]+x[1])
        return last[0]+last[1]

    def min_dest_size(self):
        """Returns the minimum size of the destination file, so that the patch can apply."""
        if len(self.hunks) == 0:
            return 0
        last = max(self.hunks, key=lambda x: x[2]+x[3])
        return last[2]+last[3]

    def read_chunks(self):
        """Iterates over arbitrary sized chunks of this patch."""
        if self.oldname is None or self.newname is None:
            raise GeneralPatchError("Patch doesn't have old or new name.")

        yield "diff --git a/%s b/%s\n" % (self.oldname, self.newname)
        yield "--- a/%s\n" % self.oldname
        yield "+++ b/%s\n" % self.newname

        for srcpos, srclines, dstpos, dstlines, hunk in self.hunks:
            yield "@@ -%d,%d +%d,%d @@\n" % (srcpos+1, srclines, dstpos+1, dstlines)
            for mode, line in hunk:
                if mode == 0:
                    yield " %s\n" % line
                elif mode == 1:
                    yield "+%s\n" % line
                elif mode == 2:
                    yield "-%s\n" % line

    def read_hunks(self, reverse=False):
        """Iterates over hunks contained in this patch, reverse exchanges source and destination."""
        for srcpos, srclines, dstpos, dstlines, hunk in self.hunks:

            srchunk = []
            dsthunk = []

            for mode, line in hunk:
                if mode == 0:
                    srchunk.append(line)
                    dsthunk.append(line)
                elif mode == 1:
                    dsthunk.append(line)
                elif mode == 2:
                    srchunk.append(line)

            assert srclines == len(srchunk)
            assert dstlines == len(dsthunk)

            if reverse:
                yield dstpos, dsthunk, srchunk
            else:
                yield srcpos, srchunk, dsthunk

class FileReader(object):
    def __init__(self, filename):
        self.filename = filename
        self.fp = open(self.filename)
        self.peeked = None

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

def read_patch(filename):
    """Iterates over all patches contained in a file, and returns FilePatch objects."""

    def _read_single_patch(fp, oldname=None, newname=None):
        patch = FilePatch(fp.filename)
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
                raise PatchParserError("Stripped old- and new name doesn't match for binary patch.")

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

                patch.hunks.append(( fp.tell(), srcpos, srclines, dstpos, dstlines ))
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
            patch.binary_patch_offset = fp.tell()
            patch.binary_patch_type = r.group(1)
            patch.binary_patch_size = int(r.group(2))

            # Skip over patch data
            while True:
                line = fp.read()
                if line is None or line.strip() == "":
                    break

        else:
            raise PatchParserError("Unknown patch format.")

        patch.offset_end = fp.tell()
        return patch

    with FileReader(filename) as fp:
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

def apply_patch(lines, patch, reverse=False, fuzz=2):
    """Apply a patch with optional fuzz - uses the commandline 'patch' utility."""

    if patch.is_empty():
        return lines

    contentfile = tempfile.NamedTemporaryFile(delete=False)
    try:
        for line in lines:
            contentfile.write("%s\n" % line)
        contentfile.close()

        patchfile = patch.extract()
        cmdline = ["patch", "--batch", "-r", "-"] # "--silent" ?
        if reverse:   cmdline.append("--reverse")
        if fuzz != 2: cmdline.append("--fuzz=%d" % fuzz)
        cmdline += [contentfile.name, patchfile.name]

        exitcode = subprocess.call(cmdline)
        if exitcode != 0:
            raise PatchApplyError("Failed to apply patch (exitcode %d)." % exitcode)

        with open(contentfile.name) as fp:
            lines = fp.read().split("\n")
            if lines[-1] == "": lines.pop()

    finally:
        os.unlink(contentfile.name)

    return lines

