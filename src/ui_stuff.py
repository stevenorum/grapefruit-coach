import base64
import json
import os

from jinja2 import Environment, FileSystemLoader
from response_core import make_response

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
    params = {"base_path":""}
    host = event.get("headers",{}).get("Host", None)
    stage = event.get("requestContext", {}).get("stage","")
    if "execute-api" in host:
        params["base_path"] = "/{}".format(stage)

    params.update(kwargs)
    return params

def get_page(template_name, event=None, **kwargs):
    return make_response(env.get_template(template_name).render(**get_params(template_name, event)))

def make_message(message, heading="Grapefruit Coach", **kwargs):
    body = env.get_template("message.html.jinja").render(message_title=heading, message_html=message)
    return make_response(body, **kwargs)

def get_static(filename, event=None, **kwargs):
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

def make_debug(event, **kwargs):
    return make_response(body="<pre>\n{}\n</pre>".format(json.dumps(event, indent=2, sort_keys=True)))
    
def make_404(event=None, **kwargs):
    return make_message("<p>I have no idea what you're talking about.</p>", heading="HTTP/404 !!1!", code=404)

def image_list(next_token=None, event=None, **kwargs):
    images = Image.scan(NextToken=next_token)
    image_links = []
