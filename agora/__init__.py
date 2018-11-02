import agora.ResourceNode
import agora.SimpleApiParser


def create_api(resources, parser=agora.SimpleApiParser.SimpleApiParser, lazyloading=True):
    """ Parse a resource descriptor and return the Resources tree associated to it """
    internal_root = parser(resources).parse()
    return agora.ResourceNode.RootResourceNode(internal_root, lazyloading=lazyloading)
