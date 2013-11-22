#!/bin/sh

PATCH_DATA="";
for FILE in patches/*.patch; do
	MD5SUM=$(md5sum "${FILE}" | sed 's| .*||g');
	AUTHOR=$(cat "${FILE}" | sed -n 's|From: \([^<]*\).*|\1|p' | sed -e 's|"||g' -e 's| $||g');
	TITLE=$(cat "${FILE}" | sed -n '1!N; s|Subject: \(.*\)\n|\1|p');
	if [ "${PATCH_DATA}" != "" ]; then
		PATCH_DATA="${PATCH_DATA}
";
	fi
	PATCH_DATA="${PATCH_DATA}+    { \"${MD5SUM}\", \"${AUTHOR}\", \"${TITLE}\" },";
done
PATCH_LINES=$(echo "${PATCH_DATA}" | grep -c '\n');
PATCH_LINES=$((${PATCH_LINES}+20));
PATCH_DATA=$(echo "${PATCH_DATA}" | sed ':a;N;$!ba;s/\n/\\n/g');
cat patch-list-template.diff | sed \
	-e "s|##PATCH_LINES##|${PATCH_LINES}|" \
	-e "s|##PATCH_DATA##|${PATCH_DATA}|"
#
