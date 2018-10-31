import agora.ResourceNode
import agora.SimpleApiParser


def create_api(resources, parser=agora.SimpleApiParser.SimpleApiParser, lazyloading=True):
    """ Parse a resource descriptor and return the Resources tree associated to it """
    internalRoot = parser(resources).parse()
    return agora.ResourceNode.RootResourceNode(internalRoot,lazyloading=lazyloading)
