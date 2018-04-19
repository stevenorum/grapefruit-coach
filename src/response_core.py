import copy
import re

def make_response(body, code=200, headers={"Content-Type": "text/html"}, base64=False):
    return {
        "body": body,
        "statusCode": code,
        "headers": headers,
        "isBase64Encoded": base64
    }

class EventMatcher(object):
    def __init__(self, response_function, default_kwargs={}, matcher_function=None):
        self.response_function = response_function
        self.kwargs = default_kwargs
        if matcher_function:
            self.matcher_function = matcher_function
        
    def match_event(self, event):
        resp = self.matcher_function(event)
        if resp:
            if len(resp) == 1:
                return (self.response_function, copy.deepcopy(self.kwargs))
            else:
                kwargs = copy.deepcopy(self.kwargs)
                kwargs.update(resp[1])
                kwargs["event"] = event if "event" not in kwargs else kwargs.get("event")
                return (self.response_function, kwargs)
        return None

class PathMatcher(EventMatcher):
    def __init__(self, regex, function, default_kwargs={}):
        super().__init__(function, default_kwargs)
        self.matcher = re.compile(regex)

    def matcher_function(self, event):
        path = event.get("path")
        response = self.matcher.match(path)
        if response:
            return (True, response.groupdict())
        return False
