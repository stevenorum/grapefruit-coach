import boto3
import ui_stuff

from response_core import PathMatcher

MATCHERS = [
    PathMatcher(r"^/?$", ui_stuff.get_page, {"template_name":"index.html"}),
    PathMatcher(r"^/?(?P<filename>static/.*)$", ui_stuff.get_static),
    PathMatcher(r"^/?(?P<template_name>[-0-9a-zA-Z_]*.htm(l)?)$", ui_stuff.get_page),
    PathMatcher(r"^/?images/?$", ui_stuff.image_list),
    PathMatcher(r"^/?images/(?P<next_token>[-_0-9a-zA-Z=%]*)$", ui_stuff.image_list),
    PathMatcher(r".*debug.*", ui_stuff.make_debug),
]

def handle_api_call(event, context):
    for m in MATCHERS:
        match = m.match_event(event)
        if match:
            function = match[0]
            kwargs = match[1]
            return function(**kwargs)
    return ui_stuff.make_404(event=event)

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
