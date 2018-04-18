import base64
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

def get_page(template_name, event=None):
    return env.get_template(template_name).render(**get_params(template_name, event))

def get_static(filename):
    filepath = os.path.abspath(os.path.join("/var/task",filename))
    if os.path.isfile(filepath) and filepath.startswith("/var/task/static/"):
        with open(filepath,"rb") as f:
            body = f.read()
            content_type = get_content_type(filename, body)
            return make_response(body=base64.b64encode(body), headers={"Content-Type": content_type}, base64=True)
    else:
        return make_response("404!!1!", code=404)
