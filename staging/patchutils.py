#!/usr/bin/python2
#
# Python functions to read, split and apply patches.
#
# Copyright (C) 2014-2016 Sebastian Lackner
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

import cStringIO as StringIO
import collections
import difflib
import email.header
import hashlib
import itertools
import os
import re
import shutil
import subprocess
import tempfile

_devnull = open(os.devnull, 'wb')

class PatchParserError(RuntimeError):
    """Unable to parse patch file - either an unimplemented feature, or corrupted patch."""
    pass

class PatchApplyError(RuntimeError):
    """Failed to apply/merge patch."""
    pass

class PatchDiffError(RuntimeError):
    """Failed to compute diff."""
    pass

class CParserError(RuntimeError):
    """Unable to parse C source."""
    pass

class PatchObject(object):
    def __init__(self, filename, header):
        self.patch_author       = header['author']
        self.patch_email        = header['email']
        self.patch_subject      = header['subject']
        self.patch_revision     = header.get('revision', 1)
        self.signed_off_by      = header.get('signedoffby', [])

        self.filename           = filename
        self.offset_begin       = None
        self.offset_end         = None
        self.isbinary           = False

        self.oldname            = None
        self.newname            = None
        self.modified_file      = None

        self.oldsha1            = None
        self.newsha1            = None
        self.newmode            = None

    def is_binary(self):
        return self.isbinary

    def read_chunks(self):
        """Iterates over arbitrary sized chunks of this patch."""
        assert self.offset_end >= self.offset_begin
        with open(self.filename) as fp:
            fp.seek(self.offset_begin)
            i = self.offset_end - self.offset_begin
            while i > 0:
                buf = fp.read(16384 if i > 16384 else i)
                if buf == "": raise IOError("Unable to extract patch.")
                yield buf
                i -= len(buf)

class _FileReader(object):
    def __init__(self, filename, content=None):
        self.filename = filename
        self.peeked   = None

        if content is not None:
            self.fp = StringIO.StringIO(content)
        else:
            self.fp = open(filename)

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

def _read_single_patch(fp, header, oldname=None, newname=None):
    """Internal function to read a single patch from a file."""

    patch = PatchObject(fp.filename, header)
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

            try:
                while srclines > 0 or dstlines > 0:
                    line = fp.read()[0]
                    if line == " ":
                        if srclines == 0 or dstlines == 0:
                            raise PatchParserError("Corrupted patch.")
                        srclines -= 1
                        dstlines -= 1
                    elif line == "-":
                        if srclines == 0:
                            raise PatchParserError("Corrupted patch.")
                        srclines -= 1
                    elif line == "+":
                        if dstlines == 0:
                            raise PatchParserError("Corrupted patch.")
                        dstlines -= 1
                    elif line == "\\":
                        pass # ignore
                    else:
                        raise PatchParserError("Unexpected line in hunk.")
            except TypeError: # triggered by None[0]
                raise PatchParserError("Truncated patch.")

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

def _parse_author(author):
    author = ' '.join([data.decode(format or 'utf-8').encode('utf-8') for \
                      data, format in email.header.decode_header(author)])
    r =  re.match("\"?([^\"]*)\"? <(.*)>", author)
    if r is None: raise NotImplementedError("Failed to parse From - header.")
    return r.group(1).strip(), r.group(2).strip()

def _parse_subject(subject):
    version = "(v|try|rev|take) *([0-9]+)"
    subject = subject.strip()
    if subject.endswith("."): subject = subject[:-1]
    r = re.match("^\\[PATCH([^]]*)\\](.*)$", subject, re.IGNORECASE)
    if r is not None:
        subject = r.group(2).strip()
        r = re.search(version, r.group(1), re.IGNORECASE)
        if r is not None: return subject, int(r.group(2))
    r = re.match("^(.*)\\(%s\\)$" % version, subject, re.IGNORECASE)
    if r is not None: return r.group(1).strip(), int(r.group(3))
    r = re.match("^(.*)\\[%s\\]$" % version, subject, re.IGNORECASE)
    if r is not None: return r.group(1).strip(), int(r.group(3))
    r = re.match("^(.*)[.,] +%s$" % version, subject, re.IGNORECASE)
    if r is not None: return r.group(1).strip(), int(r.group(3))
    r = re.match("^([^:]+) %s: (.*)$" % version, subject, re.IGNORECASE)
    if r is not None: return "%s: %s" % (r.group(1), r.group(4)), int(r.group(3))
    r = re.match("^(.*) +%s$" % version, subject, re.IGNORECASE)
    if r is not None: return r.group(1).strip(), int(r.group(3))
    r = re.match("^(.*)\\(resend\\)$", subject, re.IGNORECASE)
    if r is not None: return r.group(1).strip(), 1
    return subject, 1

def read_patch(filename, content=None):
    """Iterates over all patches contained in a file, and returns PatchObject objects."""

    header = {}
    with _FileReader(filename, content) as fp:
        while True:
            line = fp.peek()
            if line is None:
                break

            elif line.startswith("From: "):
                header['author'], header['email'] = _parse_author(line[6:])
                header.pop('signedoffby', None)
                assert fp.read() == line

            elif line.startswith("Subject: "):
                subject = line[9:].rstrip("\r\n")
                assert fp.read() == line
                while True:
                    line = fp.peek()
                    if not line.startswith(" "): break
                    subject += line.rstrip("\r\n")
                    assert fp.read() == line
                subject, revision = _parse_subject(subject)
                if not subject.endswith("."): subject += "."
                subject = re.sub('^([^:]*: *)([a-z])', lambda x: "%s%s" %
                                 (x.group(1), x.group(2).upper()), subject, 1)
                header['subject'], header['revision'] = subject, revision
                header.pop('signedoffby', None)

            elif line.startswith("Signed-off-by: "):
                if not header.has_key('signedoffby'):
                    header['signedoffby'] = []
                header['signedoffby'].append(_parse_author(line[15:]))
                assert fp.read() == line

            elif line.startswith("diff --git "):
                tmp = line.strip().split(" ")
                if len(tmp) != 4: raise PatchParserError("Unable to parse git diff header line '%s'." % line)
                yield _read_single_patch(fp, header, tmp[2].strip(), tmp[3].strip())

            elif line.startswith("--- "):
                yield _read_single_patch(fp, header)

            elif line.startswith("@@ -") or line.startswith("+++ "):
                raise PatchParserError("Patch didn't start with a git or diff header.")

            else:
                assert fp.read() == line

def apply_patch(original, patchfile, reverse=False, fuzz=2):
    """Apply a patch with optional fuzz - uses the commandline 'patch' utility."""

    result = tempfile.NamedTemporaryFile(delete=False)
    try:
        # We open the file again to avoid race-conditions with multithreaded reads
        with open(original.name) as fp:
            shutil.copyfileobj(fp, result)
        result.close()

        cmdline = ["patch", "--no-backup-if-mismatch", "--force", "--silent", "-r", "-"]
        if reverse:   cmdline.append("--reverse")
        if fuzz != 2: cmdline.append("--fuzz=%d" % fuzz)
        cmdline += [result.name, patchfile.name]

        exitcode = subprocess.call(cmdline, stdout=_devnull, stderr=_devnull)
        if exitcode != 0:
            raise PatchApplyError("Failed to apply patch (exitcode %d)." % exitcode)

        # Hack - we can't keep the file open while patching ('patch' might rename/replace
        # the file), so create a new _TemporaryFileWrapper object for the existing path.
        return tempfile._TemporaryFileWrapper(file=open(result.name, 'r+b'), \
                                              name=result.name, delete=True)
    except:
        os.unlink(result.name)
        raise

def _preprocess_source(fp):
    """Simple C preprocessor to determine where we can safely add #ifdef instructions."""

    _re_state0 = re.compile("(\"|/[/*])")
    _re_state1 = re.compile("(\\\\\"|\\\\\\\\|\")")
    _re_state2 = re.compile("\\*/")

    # We need to read the original file, and figure out where lines can be splitted
    lines = []
    for line in fp:
        lines.append(line.rstrip("\n"))

    split = set([0])
    state = 0

    i = 0
    while i < len(lines):

        # Read a full line (and handle line continuation)
        line = lines[i]
        i += 1
        while line.endswith("\\"):
            if i >= len(lines):
                raise CParserError("Unexpected end of file.")
            line = line[:-1] + lines[i]
            i += 1

        # To find out where we can add our #ifdef tags we use a simple
        # statemachine. This allows finding the beginning of a multiline
        # instruction or comment.
        j = 0
        while True:

            # State 0: No context
            if state == 0:
                match = _re_state0.search(line, j)
                if match is None: break

                if match.group(0) == "\"":
                    state = 1 # Begin of string
                elif match.group(0) == "/*":
                    state = 2 # Begin of comment
                elif match.group(0) == "//":
                    break # Rest of the line is a comment, which can be safely ignored
                else:
                    assert 0

            # State 1: Inside of string
            elif state == 1:
                match = _re_state1.search(line, j)
                if match is None:
                    raise CParserError("Line ended in the middle of a string.")

                if match.group(0) == "\"":
                    state = 0 # End of string
                elif match.group(0) != "\\\"" and match.group(0) != "\\\\":
                    assert 0

            # State 2: Multiline comment
            elif state == 2:
                match = _re_state2.search(line, j)
                if match is None: break

                if match.group(0) == "*/":
                    state = 0 # End of comment
                else:
                    assert 0

            else:
                raise CParserError("Internal state error.")
            j = match.end()

        # Only in state 0 (no context) we can split here
        if state == 0:
            split.add(i)

    # Ensure that the last comment is properly terminated
    if state != 0:
        raise CParserError("Unexpected end of file.")
    return lines, split

def generate_ifdef_patch(original, patched, ifdef):
    """Generate a patch which adds #ifdef where necessary to keep both the original and patched version."""

    #
    # The basic of idea of this algorithm is as following:
    #
    # (1) determine diff between original file and patched file
    # (2) run the preprocessor, to determine where #ifdefs can be safely added
    # (3) use diff and preprocessor information to create a merged version containing #ifdefs
    # (4) create another diff to apply the changes on the patched version
    #

    with tempfile.NamedTemporaryFile() as diff:
        exitcode = subprocess.call(["diff", "-u", original.name, patched.name],
                                   stdout=diff, stderr=_devnull)
        if exitcode == 0:
            return None
        elif exitcode != 1:
            raise PatchDiffError("Failed to compute diff (exitcode %d)." % exitcode)

        # Preprocess the original C source
        original.seek(0)
        lines, split = _preprocess_source(original)

        # Parse the created diff file
        diff.flush()
        diff.seek(0)

        # We expect this output format from 'diff', if this is not the case things might go wrong.
        line = diff.readline()
        assert line.startswith("--- ")
        line = diff.readline()
        assert line.startswith("+++ ")

        hunks = []
        while True:
            line = diff.readline()
            if line == "":
                break

            # Parse each hunk, and extract the srclines and dstlines. This algorithm is very
            # similar to _read_single_patch.
            if not line.startswith("@@ -"):
                raise PatchParserError("Unable to parse line '%s'." % line)

            r = re.match("^@@ -(([0-9]+),)?([0-9]+) \+(([0-9]+),)?([0-9]+) @@", line)
            if not r: raise PatchParserError("Unable to parse hunk header '%s'." % line)
            srcpos = max(int(r.group(2)) - 1, 0) if r.group(2) else 0
            dstpos = max(int(r.group(5)) - 1, 0) if r.group(5) else 0
            srclines, dstlines = int(r.group(3)), int(r.group(6))
            if srclines <= 0 and dstlines <= 0:
                raise PatchParserError("Empty hunk doesn't make sense.")

            srcdata = []
            dstdata = []

            try:
                while srclines > 0 or dstlines > 0:
                    line = diff.readline().rstrip("\n")
                    if line[0] == " ":
                        if srclines == 0 or dstlines == 0:
                            raise PatchParserError("Corrupted patch.")
                        srcdata.append(line[1:])
                        dstdata.append(line[1:])
                        srclines -= 1
                        dstlines -= 1
                    elif line[0] == "-":
                        if srclines == 0:
                            raise PatchParserError("Corrupted patch.")
                        srcdata.append(line[1:])
                        srclines -= 1
                    elif line[0] == "+":
                        if dstlines == 0:
                            raise PatchParserError("Corrupted patch.")
                        dstdata.append(line[1:])
                        dstlines -= 1
                    elif line[0] == "\\":
                        pass # ignore
                    else:
                        raise PatchParserError("Unexpected line in hunk.")
            except IndexError: # triggered by ""[0]
                raise PatchParserError("Truncated patch.")

            # Ensure that the patch would really apply in practice
            if lines[srcpos:srcpos + len(srcdata)] != srcdata:
                raise PatchParserError("Patch failed to apply.")

            # Strip common lines from the beginning and end
            while len(srcdata) > 0 and len(dstdata) > 0 and \
                    srcdata[0] == dstdata[0]:
                srcdata.pop(0)
                dstdata.pop(0)
                srcpos += 1
                dstpos += 1

            while len(srcdata) > 0 and len(dstdata) > 0 and \
                    srcdata[-1] == dstdata[-1]:
                srcdata.pop()
                dstdata.pop()

            # Ensure that diff generated valid output
            assert len(srcdata) > 0 or len(dstdata) > 0

            # If this is the first hunk, then check if we have to extend it at the beginning
            if len(hunks) == 0:
                assert srcpos == dstpos
                while srcpos > 0 and srcpos not in split:
                    srcpos -= 1
                    dstpos -= 1
                    srcdata.insert(0, lines[srcpos])
                    dstdata.insert(0, lines[srcpos])
                hunks.append((srcpos, dstpos, srcdata, dstdata))

            # Check if we can merge with the previous hunk
            else:
                prev_srcpos, prev_dstpos, prev_srcdata, prev_dstdata = hunks[-1]
                prev_endpos = prev_srcpos + len(prev_srcdata)

                found = 0
                for i in xrange(prev_endpos, srcpos):
                    if i in split:
                        found += 1

                # At least two possible splitting positions inbetween
                if found >= 2:
                    while prev_endpos not in split:
                        prev_srcdata.append(lines[prev_endpos])
                        prev_dstdata.append(lines[prev_endpos])
                        prev_endpos += 1

                    while srcpos not in split:
                        srcpos -= 1
                        srcdata.insert(0, lines[srcpos])
                        dstdata.insert(0, lines[srcpos])
                    hunks.append((srcpos, dstpos, srcdata, dstdata))

                # Merge hunks
                else:
                    while prev_endpos < srcpos:
                        prev_srcdata.append(lines[prev_endpos])
                        prev_dstdata.append(lines[prev_endpos])
                        prev_endpos += 1
                    assert prev_dstpos + len(prev_dstdata) == dstpos
                    prev_srcdata.extend(srcdata)
                    prev_dstdata.extend(dstdata)

            # Ready with this hunk
            pass

        # We might have to extend the last hunk
        if len(hunks):
            prev_srcpos, prev_dstpos, prev_srcdata, prev_dstdata = hunks[-1]
            prev_endpos = prev_srcpos + len(prev_srcdata)

            while prev_endpos < len(lines) and prev_endpos not in split:
                prev_srcdata.append(lines[prev_endpos])
                prev_dstdata.append(lines[prev_endpos])
                prev_endpos += 1

        # We don't need the diff anymore, all hunks are in memory
        diff.close()

    # Generate resulting file with #ifdefs
    with tempfile.NamedTemporaryFile() as intermediate:

        pos = 0
        while len(hunks):
            srcpos, dstpos, srcdata, dstdata = hunks.pop(0)
            if pos < srcpos:
                intermediate.write("\n".join(lines[pos:srcpos]))
                intermediate.write("\n")

            if len(srcdata) and len(dstdata):
                intermediate.write("#if defined(%s)\n" % ifdef)
                intermediate.write("\n".join(dstdata))
                intermediate.write("\n#else  /* %s */\n" % ifdef)
                intermediate.write("\n".join(srcdata))
                intermediate.write("\n#endif /* %s */\n" % ifdef)

            elif len(srcdata):
                intermediate.write("#if !defined(%s)\n" % ifdef)
                intermediate.write("\n".join(srcdata))
                intermediate.write("\n#endif /* %s */\n" % ifdef)

            elif len(dstdata):
                intermediate.write("#if defined(%s)\n" % ifdef)
                intermediate.write("\n".join(dstdata))
                intermediate.write("\n#endif /* %s */\n" % ifdef)

            else:
                assert 0
            pos = srcpos + len(srcdata)

        if pos < len(lines):
            intermediate.write("\n".join(lines[pos:]))
            intermediate.write("\n")
        intermediate.flush()

        # Now we can finally compute the diff between the patched file and our intermediate file
        diff = tempfile.NamedTemporaryFile()
        exitcode = subprocess.call(["diff", "-u", patched.name, intermediate.name],
                                   stdout=diff, stderr=_devnull)
        if exitcode != 1: # exitcode 0 cannot (=shouldn't) happen in this situation
            raise PatchDiffError("Failed to compute diff (exitcode %d)." % exitcode)

        diff.flush()
        diff.seek(0)

        # We expect this output format from 'diff', if this is not the case things might go wrong.
        line = diff.readline()
        assert line.startswith("--- ")
        line = diff.readline()
        assert line.startswith("+++ ")

    # Return the final diff
    return diff
