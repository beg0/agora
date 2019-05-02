# vim: set syntax=python:
# vim: set ts=4 sts=4 sw=4 et:
# AGORA Another Generator Of Rest Api
# Copyright (c) 2018, 2019 - beg0
#

""" Handle Swagger 2.0 files in AGORA. """

import re
import flex
import flex.core

from agora.InternalNode import InternalNode

SWAGGER_VARNAME_RE = re.compile("^\\{(.*)\\}$")

class SwaggerParser(object):
    """ A parser for Swagger 2.0 file

    For more information on Swagger, see:
     - https://swagger.io/
     - https://github.com/OAI/OpenAPI-Specification/blob/master/versions/2.0.md

    """

    def __init__(self, description):
        self.file = description

    def parse(self):
        """ Parse the Swager file and return the InternalNode hierarchy from it """
        schema = flex.load(self.file)
        paths = schema['paths']

        root = InternalNode("", None)

        def request_validator(req):
            """ callback used to validate a request """
            flex.core.validate_api_request(schema, req)

        def response_validator(reply, request_method='get', raw_request=None):
            """ callback used to validate a server response """
            flex.core.validate_api_response(schema, reply,
                                            request_method=request_method,
                                            raw_request=raw_request)

        for path in paths:

            url_parts = path.split("/")

            # get the final node
            #TODO: resolve '$ref' in path
            parent = root
            for part in url_parts:
                if not part:
                    continue

                #if part == '$ref':
                #    raise UnimplementedError("Swagger Parser does not support $ref")

                #Internal Node identify variable with '${.*}', Swagger with '/{.*}'
                part = SWAGGER_VARNAME_RE.sub("${\\1}", part)

                child = parent.add_child(part)
                parent = child

            resource = paths[path]
            for verb in resource:
                parent.add_method(verb,
                                  request_validator=request_validator,
                                  response_validator=response_validator)
        return root
