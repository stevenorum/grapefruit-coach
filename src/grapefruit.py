import boto3
import json

def make_response(body, code=200, headers={"Content-Type": "text/html"}, base64=False):
    return {
        "body": body,
        "statusCode": code,
        "headers": headers,
        "isBase64Encoded": base64
    }

def lambda_handler(event, context):
    return make_response(body="<pre>\n{}\n</pre>".format(json.dumps(event, indent=2, sort_keys=True)))
