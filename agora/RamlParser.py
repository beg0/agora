# vim: set syntax=python:
# vim: set ts=4 sts=4 sw=4 et:
# AGORA Another Generator Of Rest Api
# (c) 2018 - beg0
#

""" Handle RAML files in AGORA. """

import re
from pyraml import parser as prp
from agora.InternalNode import InternalNode


RAML_VARNAME_RE = re.compile("^\\{(.*)\\}$")

class RamlParser(object):
    """ A parser for RAML file """
    def __init__(self, description_file):
        self.file = description_file

    def _parse_resource(self, parent, name, node):

        # Remove leading "/". They are present in RAML but not for InternalNode
        if name[0] == "/":
            name = name[1:]

        #Internal Node identify variable with '${.*}', RAML with '/{.*}'
        name = RAML_VARNAME_RE.sub("${\\1}", name)


        child = parent.add_child(name)

        if node is not None:
            if node.methods is not None:
                for method in node.methods:
                    child.add_method(method)

            child.set_doc(node.description)

            if node.resources is not None:
                for res_name in node.resources:
                    res = node.resources[res_name]
                    self._parse_resource(child, res_name, res)

    def parse(self):
        """ Parse the RAML file and return the InternalNode hierarchy from it """
        description = prp.load(self.file)


        root = InternalNode("", None)

        if '/' in description.resources:
            res = description.resources['/']
            del description.resources['/']

            if res is not None:
                #FIXME: this duplicate code from _parse_resource
                if res.methods is not None:
                    for method in res.methods:
                        root.add_method(method)

                root.set_doc(res.description)


        if description.resources is not None:
            for name in description.resources:
                res = description.resources[name]
                self._parse_resource(root, name, res)

        return root
