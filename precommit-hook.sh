#!/bin/bash
# Installation: ln -s ../../precommit-hook.sh .git/hooks/pre-commit

git diff --cached --name-status | while read status file; do
	if [[ "$file" =~ ^patches/ ]] || [[ "$file" =~ ^debian/tools/generate-patchlist.sh$ ]]; then
		echo ""
		echo "*** GENERATING patch-list.patch ***"
		echo ""
		debian/tools/generate-patchlist.sh > patches/patch-list.patch || exit 1
		git add patches/patch-list.patch || exit 1
		break;
	fi
done
