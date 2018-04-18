from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('/var/task/jinja_templates/'))

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
