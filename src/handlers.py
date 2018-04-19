import json
import logging
import sys

root = logging.getLogger()
root.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)

for noisy in ('botocore', 'boto3', 'requests'):
    logging.getLogger(noisy).level = logging.WARN

import api_stuff
import s3_stuff

def apigateway_handler(event, context):
    print(json.dumps(event))
    return api_stuff.handle_api_call(event, context)

def s3_handler(event, context):
    print(json.dumps(event))
    return s3_stuff.handle_s3_event(event, context)
