# vim: set syntax=python:
# vim: set ts=4 sts=4 sw=4 et:
# AGORA Another Generator Of Rest Api
# (c) 2018 - beg0
#

""" Methods to do HTTP requests for standard REST verbs. """

import json
import requests


METHOD_TO_FUNCTIONS = {}

_request_mapper = {
    "GET":    lambda full_url, data: requests.get(    full_url, params=data),
    "POST":   lambda full_url, data: requests.post(   full_url, json=data),
    "PUT":    lambda full_url, data: requests.put(    full_url, json=data),
    "DELETE": lambda full_url, data: requests.delete( full_url, params=data),
    "HEAD":   lambda full_url, data: requests.head(   full_url, params=data),
    "PATCH":  lambda full_url, data: requests.patch(  full_url, json=data)
    # Note: RAML also define the following verbs
    #OPTIONS
}

def _http_method_generator(verb):
    request_fct = _request_mapper[verb]
    def http_method(self, **kwargs):
        """ Do the HTTP request for a given verb and return the replied json object """
        if verb in self.internal_node.input_validator:
            validator = self.internal_node.input_validator
            validator(kwargs)

        reply = request_fct(self.url, kwargs)
        ret = None
        if reply is not None and reply.status_code >= 200 and reply.status_code < 300 and reply.text:
            ret = reply.json()
        return ret

    # Update docstring to reflect the HTTP verb
    http_method.__doc__ = """ Do the HTTP  """ + verb + """ request and return the replied json object """
    return http_method


# Populate METHOD_TO_FUNCTIONS
for verb in _request_mapper:
    METHOD_TO_FUNCTIONS[verb] = _http_method_generator(verb)

# Cleanup
del _http_method_generator
del _request_mapper
