#!/bin/bash
# Installation: ln -s ../../precommit-hook.sh .git/hooks/pre-commit

git diff --cached --name-status | while read status file; do
	if [[ "$file" =~ ^patches/ ]] || [[ "$file" =~ ^patch-list-template.diff$ ]]; then
		echo ""
		echo "*** GENERATING patch-list.patch ***"
		echo ""
		./generate-patchlist.sh > patches/patch-list.patch || exit 1
		git add patches/patch-list.patch || exit 1
		break;
	fi
done
