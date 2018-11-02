# vim: set syntax=python:
# vim: set ts=4 sts=4 sw=4 et:
# AGORA Another Generator Of Rest Api
# (c) 2018 - beg0
#

""" Classes that are used in public API to represent the resource tree. """
import sys

from agora.HttpMethods import METHOD_TO_FUNCTIONS

def debug(*msg):
    """ Helper method to print debug message """
    if False:
        for part in msg:
            sys.stderr.write(str(part))
        sys.stderr.write("\n")

class ResourceNode(object):
    """ Represent a resource in a REST API
    This exposes every actions that can be done on such a resource.
    Depending on resource, actions that can be done may vary. ResourceNode automatically adjust
    depending on the resource.

    This is the public part of AGORA. """
    def __init__(self, parent, internal_node, lazyloading=True):
        #self.url=internal_node.get_url()


        self.parent = parent
        self.internal_node = internal_node
        self.lazyloading = lazyloading

        self.param_children = {}

        for method in internal_node.methods:
            verb = method.verb
            assert verb in METHOD_TO_FUNCTIONS, "%s is invalid verb" % verb
            unbound = METHOD_TO_FUNCTIONS[verb]
            bound = unbound.__get__(self, ResourceNode)

            self.__setattr__(verb.lower(), bound)

        #if internal_node.doc is not None:
        #    self.__doc__ = internal_node.doc
        #else:
        #    self.__doc__ = "Node for url %s." % self.url


        self._update_url()

        # create all (non-param) children, unless lasyloading is enabled
        if lazyloading is False:
            for attr in self.internal_node.children:
                self.__getattr__(attr)

    def __call__(self, *lst, **kwargs):
        if len(lst) > 0 and len(kwargs) > 0:
            raise TypeError("Except at max one positional argument or one named argument " +
                            "(exclusive). Got %d positional and %d named arguments" % \
                            (len(lst), len(kwargs)))

        if len(lst) == 0 and len(kwargs) == 0:
            return self

        param_name = None
        param_value = None

        # If there is only one param child and user only give the value, automatically deduce
        # the param name
        if len(lst) == 1:
            if len(self.internal_node.param_children) < 1:
                raise TypeError("There is no parameter for this URL")
            elif len(self.internal_node.param_children) > 1:
                raise TypeError("Can't deduce parameter name: too many possibilities")
            else:
                # Right usage of the API
                param_name = next(iter(self.internal_node.param_children))
                param_value = lst[0]
        elif len(lst) != 0:
            raise TypeError("Too many positional agument, except at max one")

        if len(kwargs) == 1:
            param_name = next(iter(kwargs))
            param_value = kwargs[param_name]
        elif len(kwargs) != 0:
            raise TypeError("Too many named arguments, except at max one")

        debug("call for '%s'='%s'" % (param_name, param_value))

        if param_name in self.internal_node.param_children:
            if param_name not in self.param_children:
                self.param_children[param_name] = {}

            if param_value in self.param_children[param_name]:
                return self.param_children[param_name][param_value]
            else:
                debug("created")

                child = ParamResourceNode(self,
                                          self.internal_node.param_children[param_name],
                                          param_value,
                                          lazyloading=self.lazyloading)

                self.param_children[param_name][param_value] = child
                return child
        else:
            raise TypeError("No such parameter %s" % param_name)



    def __getattr__(self, attr):
        debug("ask for", attr)
        try:
            child_internal_node = self.internal_node.children[attr]
            child = ResourceNode(self, child_internal_node, lazyloading=self.lazyloading)
            self.__dict__[attr] = child
            return child
        except KeyError: # no such child, let object.__getattribute__
                         # generates the exception/error message
            return object.__getattribute__(self, attr)

    def _update_url(self):
        if self.parent:
            self.url = self.parent.url + "/" + self.internal_node.name
        else:
            self.url = self.internal_node.name

        self._update_children_url()

    def _update_children_url(self):
        for child_name in self.internal_node.children:
            if child_name in self.__dict__:
                self.__dict__[child_name]._update_url()

        for param_name in self.param_children:
            for param_value in self.param_children[param_name]:
                child = self.param_children[param_name][param_value]
                child._update_url()

class ParamResourceNode(ResourceNode):
    """ A Resource Node for resource which url depend on a paramter

    e.g a resource which url looks like /user/{user}/photo
    """
    def __init__(self, parent, internal_node, value, lazyloading=True):
        self.value = value
        super(ParamResourceNode, self).__init__(parent, internal_node, lazyloading=lazyloading)

        self._update_url()

    def _update_url(self):
        if self.parent:
            self.url = self.parent.url + "/" + str(self.value)
        else:
            self.url = str(self.value)



class RootResourceNode(ResourceNode):
    """ The Resource Node that is the root of all other resources
    """
    def __init__(self, internal_root, lazyloading=True):
        super(RootResourceNode, self).__init__(None, internal_root, lazyloading=lazyloading)

    def set_base_url(self, base_url):
        """ Set the base URL to use for every resources in the resource tree """

        if base_url[-1] == '/':
            base_url = base_url[:-1]
        self.url = base_url
        self._update_children_url()
