#!/bin/bash

# linux: md5sum
# mac: md5
export MD5CMD=$(which md5sum)
which md5sum > /dev/null || export MD5CMD=$(which md5)

hash_errything() {
    find static/* | sort | while read fname ; do
        cat $fname | $MD5CMD
    done
}

CHECKSUM=$(hash_errything | $MD5CMD)

aws s3 sync static s3://$STATIC_BUCKET/$CHECKSUM/static

echo "{\"STATIC_BUCKET\":\"$STATIC_BUCKET\",\"STATIC_PATH\":\"$CHECKSUM\"}" > $1
