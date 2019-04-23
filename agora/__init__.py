# vim: set syntax=python:
# vim: set ts=4 sts=4 sw=4 et:
# AGORA Another Generator Of Rest Api
# Copyright (c) 2018, 2019 - beg0
#

""" AGORA Another Generator Of Rest Api. """

import agora.ResourceNode
import agora.SimpleApiParser


def create_api(resources, parser=agora.SimpleApiParser.SimpleApiParser,
        lazyloading=True,
        enable_request_validator=True,
        enable_response_validator=True):
    """ Parse a resource descriptor and return the Resources tree associated to it """
    internal_root = parser(resources).parse()
    return agora.ResourceNode.RootResourceNode(internal_root, lazyloading=lazyloading,
        enable_request_validator=enable_request_validator,
        enable_response_validator=enable_response_validator)
