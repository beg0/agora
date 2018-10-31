# vim: set syntax=python:
# vim: set ts=4 sts=4 sw=4 et:
# AGORA Another Generator Of Rest Api
# (c) 2018 - beg0
#
from agora.InternalNode import InternalNode

class SimpleApiParser(object):
    """ A Simple (e.g. light) API parser
    Used when your API is very light and you don't have an external file to define it (unlike
    Swagger or RAML)

    Your API should be defined in a simple list as below:
    resources=[
            { "url": "/user/", "method": "get" },
            { "url": "/user/", "method": "post" },
            { "url": "/user/${username}", "method": "get" },
            { "url": "/user/${username}", "method": "put" },
            { "url": "/user/${username}", "method": "delete" },
            { "url": "/user/${username}/friend", "method": "get" },
            { "url": "/user/${username}/friend", "method": "post" },
            { "url": "/user/${username}/friend/${friendname}", "method": "get" },
            { "url": "/user/${username}/friend/${friendname}", "method": "delete" }
            ]

        API = createApi(resources, parser=SimpleApiParser)
            """

    def __init__(self, resources_list):
        assert isinstance(resources_list, list), \
            "must be a list of resource, got %s" % type(resources_list).__name__

        for res in resources_list:
            assert isinstance(res, dict)
            assert "url" in res and isinstance(res["url"], str) and len(res["url"]) > 0


        self.resources = resources_list

    def parse(self):
        """ Parse the resources list and return the InternalNode hierarchy from it """
        root = InternalNode("", None)

        for res in self.resources:
            url = res["url"]
            parts = url.split("/")
            parent = root
            for part in parts:
                if not part:
                    continue
                child = parent.add_child(part)
                parent = child

            if "method" in res:
                parent.add_method(res["method"])
            if "doc" in res:
                parent.set_doc(res["doc"])
        return root
