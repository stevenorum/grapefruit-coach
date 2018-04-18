import boto3
import json

import ui_stuff

from response_core import make_response

def handle_api_call(event, context):
    path = event.get("path")
    if path in ["","/","index.html","/index.html"]:
        return make_response(ui_stuff.get_page("index.html", event=event))
    if path.startswith("/static"):
        return ui_stuff.get_static(path[1:])
    return make_response(body="<pre>\n{}\n</pre>".format(json.dumps(event, indent=2, sort_keys=True)))

'''

Paths that need to be supported:

GET train - Page that lets you annotate a randomly chosen image.  (This will likely be a redirect to the next line's URL.)
GET train/<image_id> - Page that lets you annotate that specific image.
POST train/<image_id> - API to record an object in an image.

POST images/from_url - API to receive a URL and add the image at that location to the library.
POST images/upload - API to get a presigned upload link
GET images/list(/<start_token>) - Page that lists all the images known so far.
GET image/<image_id> - View an image, and all the objects annotated so far.

What else?

'''
