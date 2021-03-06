#!/bin/bash

if [ -z "$MD5CMD" ] ; then
    MD5CMD="md5sum"
fi

hash_everything() {
    find static/* | sort | while read fname ; do
        cat $fname | $MD5CMD | grep -o "[0-9a-f]{32}"
    done
}

CHECKSUM=$(hash_everything | $MD5CMD | grep -o "[0-9a-f]\{32\}")
echo "Checksum: '$CHECKSUM'"

if [ -z "$AWS_PROFILE" ] ; then
    aws s3 sync static s3://$STATIC_BUCKET/$CHECKSUM/static
else
    aws --profile $AWS_PROFILE s3 sync static s3://$STATIC_BUCKET/$CHECKSUM/static
fi
echo "{\"STATIC_BUCKET\":\"$STATIC_BUCKET\",\"STATIC_PATH\":\"$CHECKSUM\"}"

echo "{\"STATIC_BUCKET\":\"$STATIC_BUCKET\",\"STATIC_PATH\":\"$CHECKSUM\"}" > $1
