# vim: set syntax=python:
# vim: set ts=4 sts=4 sw=4 et:
# AGORA Another Generator Of Rest Api
# (c) 2018 - beg0
#
import re
import flex

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

        for path in paths:

            urlParts = path.split("/")

            # get the final node
            #TODO: resolve '$ref' in path
            parent = root
            for part in urlParts:
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
                parent.add_method(verb)

        return root
