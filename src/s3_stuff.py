import boto3
import json
import traceback

from orm import Image

def handle_s3_event(event, context):
    for record in event.get("Records"):
        try:
            bucket = record["s3"]["bucket"]["name"]
            key = record["s3"]["object"]["key"]

            who = record["userIdentity"]["principalId"]
            what = record["eventName"]
            when = record["eventTime"]
            message = "Around {when}, user {who} performed action {what} on object {key} in bucket {bucket}".format(bucket=bucket, key=key, who=who, what=what, when=when)
            print(message)

            image = Image(image_name=key)
            image._save()

        except:
            traceback.print_exc()
            print("Error handling record.")
    pass
