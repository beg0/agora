# vim: set syntax=python:
# vim: set ts=4 sts=4 sw=4 et:
# AGORA Another Generator Of Rest Api
# (c) 2018 - beg0
#

import sys,os
import types
import unittest

for d in [os.path.realpath(os.path.join(os.path.dirname(sys.argv[0]), '..'))]:
    sys.path.insert(0,d)

from agora.RamlParser import *
from agora.InternalNode import *

class TestRamlParser(unittest.TestCase):
    samples_dir = os.path.join(
        os.path.dirname(__file__), 'samples')

    def sample_path(self, *parts):
        return os.path.join(self.samples_dir, *parts)

    def _getExpectedTree(self):
        root = InternalNode("",None)

        # / (root)
        root.add_method("head")
        root.add_method("post")
        root.set_doc("Root resource description")

        # /media
        mediaNode = root.add_child("media")
        mediaNode.add_method("head")
        mediaNode.add_method("get")

        # /media/{mediaId}
        mediaIdNode = mediaNode.add_child("${mediaId}")
        mediaIdNode.add_method("head")
        mediaIdNode.add_method("get")

        # /tags
        tagsNode = root.add_child("tags")
        tagsNode.add_method("head")

        # /tags/{tagId}
        tagIdNode = tagsNode.add_child("${tagId}")
        tagIdNode.add_method("head")
        tagIdNode.add_method("delete")

        # /foo
        fooNode = root.add_child("foo")
        fooNode.add_method("get")

        # /foo/bar
        barNode = fooNode.add_child("bar")

        # /foo/bar/subbar
        subbarNode = barNode.add_child("subbar")

        # /foo/baz
        bazNode = fooNode.add_child("baz")
        bazNode.add_method("post")

        return root

    def test_simple(self):
        rp = RamlParser(self.sample_path("full-config.yaml"))
        root=rp.parse()

        self.assertIsInstance(root, InternalNode, "parse() returns InternalNode")

        self.assertEqual(root, self._getExpectedTree(), "parse() returns the expected InternalNode tree")

        #self.assertEqual(root.name,"", "root has empty name")
        #self.assertEqual(root.parent,None, "root has no parent")
        #root_children = root.children.keys()
        #root_children.sort()
        #root_expected_children = ["media","tags","foo"]
        #root_expected_children.sort()
        #self.assertEqual(root_children, root_expected_children, "root has 3 children")
