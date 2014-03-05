#!/bin/bash

# Setup parser variables
lineno=0
verbose=0
patch_mode=0
patch_tmpfile=""

# Macros
abort()
{
	if [ ! -z "$patch_tmpfile" ]; then
		rm "$patch_tmpfile"
		patch_tmpfile=""
	fi
	echo "[PATCH:$lineno] ERR: $1" >&2
	exit 1
}

invalid_parser_state()
{
	abort "Invalid parser state (patch_mode=$patch_mode)!"
}

warning()
{
	echo "[PATCH:$lineno] WRN: $1" >&2
}

usage()
{
	echo ""
	echo "Usage: ./gitapply [-v] [-d DIRECTORY]"
	echo ""
	echo "Reads patch data from stdin and applies the patch to the current"
	echo "directory or the directory given via commandline."
	echo ""
	echo "The patch file can contain both unified text patches as well as"
	echo "git binary patches."
	echo ""
}

# Parse environment variables
while [[ $# > 0 ]]; do
	cmd="$1"; shift
	case "$cmd" in

		--directory=*)
			cd "${cmd#*=}"
			;;
		-d)
			cd "$1"; shift
			;;

		-R)
			abort "Reverse applying patches not supported yet with this patch tool."
			;;

		-v)
			verbose=1
			;;

		--help)
			usage
			exit 0
			;;

		*)
			warning "Unknown argument $cmd"
			;;
	esac
done

# Decode base85 git data, prepend with a gzip header
awk_b85='
BEGIN{
  git="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
  b85="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!#$%&()*+-;<=>?@^_`{|}~";
  printf("\x1f\x8b\x08\x00\x00\x00\x00\x00");
  while (getline > 0){
    l = index(git, substr($0, 1, 1)); if (l == 0){ exit 1; }; p=2;
    while (l > 0 && p <= length($0)){
      a = index(b85, substr($0, p++, 1));
      b = index(b85, substr($0, p++, 1));
      c = index(b85, substr($0, p++, 1));
      d = index(b85, substr($0, p++, 1));
      e = index(b85, substr($0, p++, 1));
      if (a-- == 0 || b-- == 0 || c-- == 0 || d-- == 0 || e-- == 0){ exit 1; }
      n = (((a * 85 + b) * 85 + c) * 85 + d) * 85 + e;
      if (n > 4294967295){ exit 1; }
      a = n % 256; n /= 256;
      b = n % 256; n /= 256;
      c = n % 256; n /= 256;
      d = n % 256;
      if (l-- > 0) printf("%c", d);
      if (l-- > 0) printf("%c", c);
      if (l-- > 0) printf("%c", b);
      if (l-- > 0) printf("%c", a);
    }
    if (p != length($0) + 1 || l != 0){ exit 1; }
  }
}'

# Decodes the information from a git delta patch passed in as hex encoded
awk_gitpatch='
function get_byte(a, b){ # usage: get_byte()
  if (length(__buffer) == 0){ if(getline __buffer <= 0){ exit 1; } }
  a = index(hex, substr(__buffer, 1, 1));
  b = index(hex, substr(__buffer, 2, 1));
  if (a-- == 0 || b-- == 0){ exit 1; }
  __buffer = substr(__buffer, 3); __pos++;
  return a * 16 + b;
}
function skip_bytes(n, m){ # usage: skip_bytes(n)
  if (length(__buffer) == 0){ if(getline __buffer <= 0){ exit 1; } }
  while (n >= (length(__buffer) / 2)){
    m = length(__buffer) / 2; n -= m; __pos += m;
    if(getline __buffer <= 0){ exit 1; }
  }
  if (n > 0){ __buffer = substr(__buffer, 1 + 2 * n); __pos += n; }
}
function get_delta_hdr_size(){ # usage: get_delta_hdr_size()
  cmd = get_byte(); size = and(cmd, 0x7f); i = 7;
  while (and(cmd, 0x80)){
    cmd = get_byte(); size += lshift(and(cmd, 0x7f), i); i += 7;
  }
  return size;
}
BEGIN{
  hex="0123456789ABCDEF"
  src_size = get_delta_hdr_size(); dst_size = get_delta_hdr_size();
  printf("S %d %d\n", src_size, dst_size);
  while (dst_size > 0){
    cmd = get_byte();
    if (and(cmd, 0x80)){
      cp_offs = 0; cp_size = 0;
      if (and(cmd, 0x01)){ cp_offs  = get_byte(); }
      if (and(cmd, 0x02)){ cp_offs += lshift(get_byte(), 8); }
      if (and(cmd, 0x04)){ cp_offs += lshift(get_byte(), 16); }
      if (and(cmd, 0x08)){ cp_offs += lshift(get_byte(), 24); }
      if (and(cmd, 0x10)){ cp_size  = get_byte(); }
      if (and(cmd, 0x20)){ cp_size += lshift(get_byte(), 8); }
      if (and(cmd, 0x40)){ cp_size += lshift(get_byte(), 16); }
      if (cp_size == 0) cp_size = 0x10000;
      if (cp_offs + cp_size > src_size || cp_size > dst_size){ exit 1; }
      printf("1 %d %d\n", cp_offs, cp_size);
      dst_size -= cp_size;
    }else if (cmd){
      if (cmd > dst_size){ exit 1; }
      printf("2 %d %d\n", __pos, cmd);
      skip_bytes(cmd);
      dst_size -= cmd;
    }else{ exit 1; }
  }
  printf("E 0 0\n");
}'

# Parse lines of the patch
while IFS= read -r line; do
	(( lineno++ ))

	# In verbose mode we print each line of the patch to stdout
	if [ "$verbose" -ne 0 ]; then
		echo "$lineno: $line"
	fi

	# MODE 1: Parse header
	# Fall-through to 2
	if [ "$patch_mode" -eq 1 ]; then
		if [[ "$line" =~ ^---\ (.*)$ ]]; then
			patch_oldname="${BASH_REMATCH[1]}"
			echo "$line" >> "$patch_tmpfile"
			continue

		elif [[ "$line" =~ ^\+\+\+\ (.*)$ ]]; then
			patch_newname="${BASH_REMATCH[1]}"
			echo "$line" >> "$patch_tmpfile"
			continue

		elif [[ "$line" =~ ^old\ mode ]] || [[ "$line" =~ ^deleted\ file\ mode ]]; then
			# ignore
			echo "$line" >> "$patch_tmpfile"
			continue

		elif [[ "$line" =~ ^new\ mode\ ([0-9]*)$ ]] || [[ "$line" =~ ^new\ file\ mode\ ([0-9]*)$ ]]; then
			patch_filemode="${BASH_REMATCH[1]}"
			echo "$line" >> "$patch_tmpfile"
			continue

		elif [[ "$line" =~ ^new\ mode ]] || [[ "$line" =~ ^new\ file\ mode ]]; then
			patch_errors+=("$lineno: unable to parse header line '$line'")
			patch_invalid=1
			echo "$line" >> "$patch_tmpfile"
			continue

		elif [[ "$line" =~ ^copy\ from ]] || [[ "$line" =~ ^copy\ to ]]; then
			patch_errors+=("$lineno: copy header not implemented yet")
			patch_invalid=1
			echo "$line" >> "$patch_tmpfile"
			continue

		elif [[ "$line" =~ ^rename\ old ]] || [[ "$line" =~ ^rename\ from ]]; then
			patch_errors+=("$lineno: rename header not implemented yet")
			patch_invalid=1
			echo "$line" >> "$patch_tmpfile"
			continue

		elif [[ "$line" =~ ^rename\ new ]] || [[ "$line" =~ ^rename\ to ]]; then
			patch_errors+=("$lineno: rename header not implemented yet")
			patch_invalid=1
			echo "$line" >> "$patch_tmpfile"
			continue

		elif [[ "$line" =~ ^similarity\ index ]] || [[ "$line" =~ ^dissimilarity\ index ]]; then
			# ignore
			echo "$line" >> "$patch_tmpfile"
			continue

		elif [[ "$line" =~ ^index\ ([a-fA-F0-9]*)\.\.([a-fA-F0-9]*) ]]; then
			patch_oldsha1="${BASH_REMATCH[1]}"
			patch_newsha1="${BASH_REMATCH[2]}"
			echo "$line" >> "$patch_tmpfile"
			continue

		elif [[ "$line" =~ ^index\  ]]; then
			patch_errors+=("$lineno: unable to parse header line '$line'")
			patch_invalid=1
			echo "$line" >> "$patch_tmpfile"
			continue

		else
			# Remove first path components, which are always a/ and b/ for git patches
			if [[ "$patch_oldname" =~ ^a/(.*)$ ]]; then
				patch_oldname="${BASH_REMATCH[1]}"
			elif [ "$patch_oldname" != "/dev/null" ]; then
				abort "old name doesn't start with a/."
			fi
			if [[ "$patch_newname" =~ ^b/(.*)$ ]]; then
				patch_newname="${BASH_REMATCH[1]}"
			elif [ "$patch_newname" != "/dev/null" ]; then
				abort "new name doesn't start with b/."
			fi

			patch_mode=2
			# fall-through
		fi
	fi

	# MODE 2: Decide between binary and textual patch data
	# Fall-through to 200, 0
	if [ "$patch_mode" -eq 2 ]; then
		if [[ "$line" == "GIT binary patch" ]]; then

			if [ -z "$patch_oldsha1" ] || [ -z "$patch_newsha1" ]; then
				patch_errors+=("$lineno: missing index header, sha1 sums required for binary patch")
				patch_invalid=1
			fi

			if [ "$patch_oldname" != "$patch_newname" ]; then
				patch_errors+=("$lineno: stripped old- and new name doesn't match")
				patch_invalid=1
			fi

			if [ "$patch_invalid" -ne 0 ]; then
				for error in "${patch_errors[@]}"; do echo "$error" >&2; done
				abort "Unable to continue."
			fi

			patch_mode=100
			continue

		elif [[ "$line" =~ ^@@\ - ]]; then
			# We count the number of lines added/removed for informational purposes
			patch_total_add=0
			patch_total_rem=0

			patch_mode=200
			# fall-through

		elif [[ "$line" =~ ^diff\ --git\  ]]; then

			if [ "$patch_oldname" != "$patch_newname" ]; then
				patch_errors+=("$lineno: stripped old- and new name doesn't match")
				patch_invalid=1
			fi

			if [ "$patch_invalid" -ne 0 ]; then
				for error in "${patch_errors[@]}"; do echo "$error" >&2; done
				abort "Unable to continue."
			fi

			if [ ! -z "$patch_filemode" ]; then
				echo "patching $patch_newname"
				chmod "${patch_filemode: -3}" "$patch_oldname" # we ignore failures for now
			fi

			patch_mode=0
			# fall-through

		elif [ ! -z "$line" ]; then
			abort "Unknown patch format."
		fi
	fi

	# MODE 100: Decide between binary literal/delta patch
	if [ "$patch_mode" -eq 100 ]; then
		if [[ "$line" =~ ^(literal|delta)\ ([0-9]+)$ ]]; then
			binary_patch_type="${BASH_REMATCH[1]}"
			binary_patch_size="${BASH_REMATCH[2]}"

			# Check shasum if its not a patch creating a new file
			if [ "$patch_oldsha1" != "0000000000000000000000000000000000000000" ] || [ "$binary_patch_type" == "delta" ] || [ -f "$patch_oldname" ]; then
				if [ -f "$patch_oldname" ]; then
					sha=$(echo -en "blob $(du -b "$patch_oldname" | cut -f1)\x00" | cat - "$patch_oldname" | sha1sum | cut -d' ' -f1)
				else
					sha="0000000000000000000000000000000000000000"
				fi
				if [ "$patch_oldsha1" != "$sha" ]; then
					echo "$lineno: Expected $patch_oldsha1"
					echo "$lineno: Got      $sha"
					abort "Unable to continue because of sha1 mismatch of original file."
				fi
			fi

			# Is it a patch deleting this file
			if [ "$patch_newsha1" == "0000000000000000000000000000000000000000" ] && [ "$binary_patch_size" -eq 0 ] && [ "$binary_patch_type" == "literal" ]; then
				echo "patching $patch_newname"

				# Apply the patch: Just delete the file
				if [ -f "$patch_oldname" ] && ! rm "$patch_oldname"; then
					abort "Unable to delete file $patch_oldname."
				fi

				# We are ready with this one
				patch_mode=0
				continue
			fi

			# Clear temporary file, we will use it to decode the binary block
			echo -en "" > "$patch_tmpfile"
			patch_mode=101
			continue

		else
			abort "Only literal/delta patches are supported."
		fi
	fi

	# MODE 101: Decode data
	if [ "$patch_mode" -eq 101 ]; then
		if [ ! -z "$line" ]; then
			# Append this binary chunk in the temp file
			echo "$line" >> "$patch_tmpfile"

		else
			echo "patching $patch_newname"

			decoded_tmpfile=$(mktemp)
			if [ ! -f "$decoded_tmpfile" ]; then
				abort "Unable to create temporary file for patch"
			fi

			# Decode base85 and add a gzip header
			awk "$awk_b85" < "$patch_tmpfile" | gzip -dc > "$decoded_tmpfile" 2>/dev/null

			# The new temp file replaces the old one
			rm "$patch_tmpfile"
			patch_tmpfile="$decoded_tmpfile"

			# Ensure that resulting binary patch has the correct size
			if [ "$binary_patch_size" -ne "$(du -b "$patch_tmpfile" | cut -f 1)" ]; then
				abort "Uncompressed data has wrong size, expected $binary_patch_size, got $size"
			fi

			# Apply git delta path
			if [ "$binary_patch_type" == "delta" ]; then

				decoded_tmpfile=$(mktemp)
				if [ ! -f "$decoded_tmpfile" ]; then
					abort "Unable to create temporary file for patch"
				fi

				binary_patch_complete=0
				binary_patch_destsize=""

				while read cmd arg1 arg2; do
					if [ "$cmd" == "S" ]; then
						binary_patch_destsize="$arg2"
						if [ "$arg1" -ne "$(du -b "$patch_oldname" | cut -f 1)" ]; then break; fi

					elif [ "$cmd" == "1" ]; then
						if ! dd if="$patch_oldname" bs=1 skip="$arg1" count="$arg2" >> "$decoded_tmpfile" 2>/dev/null; then break; fi

					elif [ "$cmd" == "2" ]; then
						if ! dd if="$patch_tmpfile" bs=1 skip="$arg1" count="$arg2" >> "$decoded_tmpfile" 2>/dev/null; then break; fi

					elif [ "$cmd" == "E" ]; then
						binary_patch_complete=1

					else break; fi
				done < <(hexdump -v -e '32/1 "%02X" "\n"' "$patch_tmpfile" | awk "$awk_gitpatch")

				# The new temp file replaces the old one
				rm "$patch_tmpfile"
				patch_tmpfile="$decoded_tmpfile"

				if [ "$binary_patch_complete" -ne 1 ]; then
					abort "Unable to parse full patch."
				elif [ "$binary_patch_destsize" -ne "$(du -b "$patch_tmpfile" | cut -f 1)" ]; then
					abort "Unpacked file has wrong length."
				fi

			elif [ "$binary_patch_type" != "literal" ]; then
				invalid_parser_state
			fi

			# Check shasum if its not a patch creating a new file
			sha=$(echo -en "blob $(du -b "$patch_tmpfile" | cut -f1)\x00" | cat - "$patch_tmpfile" | sha1sum | cut -d' ' -f1)
			if [ "$patch_newsha1" != "$sha" ]; then
				echo "$lineno: Expected $patch_newsha1"
				echo "$lineno: Got      $sha"
				abort "Unable to continue because of sha1 mismatch after applying the patch"
			fi

			if ! cp "$patch_tmpfile" "$patch_oldname"; then
				abort "Unable to replace original file"
			fi
			if [ ! -z "$patch_filemode" ]; then
				chmod "${patch_filemode: -3}" "$patch_oldname" # we ignore failures for now
			fi

			# We're ready with this patch
			patch_mode=0
			continue
		fi
	fi

	# MODE 200: Text patch
	# Fall-through to 0
	if [ "$patch_mode" -eq 200 ]; then
		hunk="^@@\ -(([0-9]+),)?([0-9]+)\ \+(([0-9]+),)?([0-9]+)\ @@"
		if [[ "$line" =~ $hunk ]]; then
			# ${BASH_REMATCH[2]} - source line
			# ${BASH_REMATCH[5]} - end line
			hunk_src_lines="${BASH_REMATCH[3]}"
			hunk_dst_lines="${BASH_REMATCH[6]}"

			if [ "$hunk_src_lines" -eq 0 ] && [ "$hunk_dst_lines" -eq 0 ]; then
				abort "Empty hunk doesn't make sense."
			fi

			# Start of a new hunk, append it
			echo "$line" >> "$patch_tmpfile"
			patch_mode=201
			continue

		else
			echo "patching $patch_newname"

			# Try to apply the patch using 'patch'
			if ! patch -p1 -s -f < "$patch_tmpfile"; then
				abort "Patch did not apply, aborting."
			fi

			patch_mode=0
			# fall-through
		fi
	fi

	# MODE 201: Wait until we reach the end of a hunk
	if [ "$patch_mode" -eq 201 ]; then
		# These lines are part of a hunk, append it
		echo "$line" >> "$patch_tmpfile"

		if [ "$hunk_src_lines" -gt 0 ] && [ "$hunk_dst_lines" -gt 0 ] && [[ "$line" =~ ^\  ]]; then
			(( hunk_src_lines-- ))
			(( hunk_dst_lines-- ))

		elif [ "$hunk_src_lines" -gt 0 ] && [[ "$line" =~ ^- ]]; then
			(( hunk_src_lines-- ))
			(( patch_total_rem++ ))

		elif [ "$hunk_dst_lines" -gt 0 ] && [[ "$line" =~ ^\+ ]]; then
			(( hunk_dst_lines-- ))
			(( patch_total_add++ ))

		elif [[ "$line" =~ ^\\\  ]]; then
			continue # ignore "\\ No newline ..."

		else
			abort "Unexpected line in hunk"
		fi

		# If it was the last line of this hunk then go back to mode 200
		if [ "$hunk_src_lines" -eq 0 ] && [ "$hunk_dst_lines" -eq 0 ]; then
			patch_mode=200
			continue
		fi
	fi

	# MODE 0: Search for patch header
	if [ "$patch_mode" -eq 0 ]; then
		if [[ "$line" =~ ^diff\ --git\ ([^ ]*)\ ([^ ]*)$  ]]; then

			# Is this patch valid? The array will contain a list of detected errors
			patch_invalid=0
			patch_errors=()

			# Setup name and sha1 sum variables
			patch_oldname="${BASH_REMATCH[1]}"
			patch_newname="${BASH_REMATCH[2]}"
			patch_oldsha1=""
			patch_newsha1=""

			# Filemode
			patch_filemode=""

			if [ ! -z "$patch_tmpfile" ]; then
				rm "$patch_tmpfile"
			fi
			patch_tmpfile=$(mktemp)
			if [ ! -f "$patch_tmpfile" ]; then
				abort "Unable to create temporary file for patch."
			fi
			echo "$line" >> "$patch_tmpfile"

			patch_mode=1
			continue

		elif [[ "$line" =~ ^@@\ - ]] || [[ "$line" =~ ^---\  ]] || [[ "$line" =~ ^\+\+\+\  ]]; then
			abort "Patch corrupted or not created with git."
		fi
	fi

done

# Apply last text patch (if any)
if [ "$patch_mode" -eq 200 ]; then
	echo "patching $patch_newname"

	# Try to apply the patch using 'patch'
	if ! patch -p1 -s -f < "$patch_tmpfile"; then
		abort "Patch did not apply, aborting."
	fi

	patch_mode=0
fi

# Make sure we're not just parsing a patch
if [ "$patch_mode" -ne 0 ]; then
	abort "File ended in the middle of a patch!"
fi

# Clean up temp files if any
if [ ! -z "$patch_tmpfile" ]; then
	rm "$patch_tmpfile"
	patch_tmpfile=""
fi

# Success
exit 0
