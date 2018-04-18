import json

import api_stuff
import s3_stuff

def apigateway_handler(event, context):
    print(json.dumps(event))
    return api_stuff.handle_api_call(event, context)

def s3_handler(event, context):
    print(json.dumps(event))
    return s3_stuff.handle_s3_event(event, context)
