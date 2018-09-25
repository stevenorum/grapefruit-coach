import base64
import json
import os
from functools import update_wrapper
from jinja2 import Environment, FileSystemLoader
from sneks.sam.response_core import make_response, redirect
from sneks import snekjson

env = Environment(loader=FileSystemLoader('/var/task/jinja_templates/'))

content_types = {
    "jpg":"image/jpg",
    "jpeg":"image/jpeg",
    "png":"image/png",
    "gif":"image/gif",
    "bmp":"image/bmp",
    "tiff":"image/tiff",
    "txt":"text/plain",
    "rtf":"application/rtf",
    "ttf":"font/ttf",
    "css":"text/css",
    "html":"text/html",
    "js":"application/javascript",
    "eot":"application/vnd.ms-fontobject",
    "svg":"image/svg+xml",
    "woff":"application/x-font-woff",
    "woff2":"application/x-font-woff",
    "otf":"application/x-font-otf",
    "json":"application/json",
    }

binary_types = [
    "image/jpg",
    "image/jpeg",
    "image/png",
    "image/gif",
    "image/bmp",
    "image/tiff",
    "font/ttf",
    "application/vnd.ms-fontobject",
    "application/x-font-woff",
    "application/x-font-otf",
]

def get_content_type(fname, body=None):
    return content_types.get(fname.split(".")[-1].lower(),"binary/octet-stream")

def get_params(template_name, event=None, **kwargs):
    params = {"event":"event"}
    params.update(event["params"]["single_kwargs"])
    params.update(event["params"]["objects"])
    params["path"] = event["params"]["path"]
    params["base_path"] = params["path"]["base"]
    params["static_base"] = params["path"]["static_base"]
    params["event"] = event
    params["this_page"] = template_name
    params.update(kwargs)
    for level in ["success","info","warning","error"]:
        sk = "{}_message".format(level)
        lk = "{}_messages".format(level)
        if lk not in params:
            params[lk] = [params[sk]] if sk in params else []
        else:
            if sk in params and params[sk] not in params[lk]:
                params[lk].append(params[sk])
    return snekjson.blob(params)

def get_page(template_name, event=None, **kwargs):
    return make_response(env.get_template(template_name).render(**get_params(template_name, event, this_page=template_name, **kwargs)))

def is_response(d):
    return len(d) == 4 and "body" in d and "statusCode" in d and "headers" in d and "isBase64Encoded" in d

def loader_for(template_name):
    def new_decorator(func):
        def newfunc(event, *args, **kwargs):
            params = func(event, *args, **kwargs)
            if is_response(params):
                return params
            return get_page(template_name, event, **params)
        update_wrapper(newfunc, func)
        return newfunc
    return new_decorator

def make_message(message, heading="Example Website", **kwargs):
    body = env.get_template("message.html.jinja").render(message_title=heading, message_html=message)
    return make_response(body, **kwargs)

def get_static(filename, event=None, **kwargs):
    if "STATIC_BUCKET" in os.environ and "STATIC_PATH" in os.environ:
        return redirect("https://s3.amazonaws.com/{STATIC_BUCKET}/{STATIC_PATH}/{filename}".format(filename=filename, **os.environ))
    filepath = os.path.abspath(os.path.join("/var/task",filename))
    if os.path.isfile(filepath) and filepath.startswith("/var/task/static/"):
        content_type = get_content_type(filename)
        b64encoded = False
        if content_type in binary_types:
            with open(filepath,"rb") as f:
                body = base64.b64encode(f.read()).decode("utf-8")
                b64encoded = True
        else:
            with open(filepath,"r") as f:
                body = f.read()
        return make_response(body=body, headers={"Content-Type": content_type}, base64=b64encoded)
    else:
        return make_response("404!!1!", code=404)

def make_debug(event=None, context=None, headers={}, **kwargs):
    templates = env.list_templates()
    return make_response(body="<pre>\n{}\n\nAvailable Jinja2 templates:\n\n{}\n</pre>".format(snekjson.dumps(event, indent=2, sort_keys=True, ignore_type_error=True).replace(">","&gt").replace("<","&lt"),"\n".join(templates)), headers=headers)

def make_404(event=None, context=None, **kwargs):
    return make_message("<p>I have no idea what you're talking about.</p>", heading="HTTP/404 !!1!", code=404)
