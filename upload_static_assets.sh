#!/bin/bash

hash_errything() {
    find static/* | sort | while read fname ; do
        cat $fname | md5sum | grep -o "[0-9a-f]{32}"
    done
}

CHECKSUM=$(hash_errything | md5sum | grep -o "[0-9a-f]{32}")
echo "Checksum: '$CHECKSUM'"

aws s3 sync static s3://$STATIC_BUCKET/$CHECKSUM/static

echo "{\"STATIC_BUCKET\":\"$STATIC_BUCKET\",\"STATIC_PATH\":\"$CHECKSUM\"}"

echo "{\"STATIC_BUCKET\":\"$STATIC_BUCKET\",\"STATIC_PATH\":\"$CHECKSUM\"}" > $1
