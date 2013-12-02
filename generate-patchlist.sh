#!/bin/sh

PATCH_DATA="";
for FILE in patches/*/*.def; do
	UUID=$(echo "${FILE}" | sed -e 's|^.*/||g' -e 's|\.def$||g');
	REVISION=$(cat "${FILE}" | sed -n 's|Revision: \(.*\)|\1|p');
	AUTHOR=$(cat "${FILE}" | sed -n 's|Author: \(.*\)|\1|p');
	TITLE=$(cat "${FILE}" | sed -n 's|Title: \(.*\)|\1|p');
	if [ "${AUTHOR}" = "" ] && [ "${TITLE}" = "" ]; then
		continue;
	fi
	if [ "${PATCH_DATA}" != "" ]; then
		PATCH_DATA="${PATCH_DATA}
";
	fi
	PATCH_DATA="${PATCH_DATA}+    { \"${UUID}:${REVISION}\", \"${AUTHOR}\", \"${TITLE}\" },";
done
PATCH_LINES=$(echo "${PATCH_DATA}" | grep -c '\n');
PATCH_LINES=$((${PATCH_LINES}+20));
PATCH_DATA=$(echo "${PATCH_DATA}" | sed ':a;N;$!ba;s/\n/\\n/g');
cat patch-list-template.diff | sed \
	-e "s|##PATCH_LINES##|${PATCH_LINES}|" \
	-e "s|##PATCH_DATA##|${PATCH_DATA}|"
#
