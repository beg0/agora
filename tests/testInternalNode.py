# vim: set syntax=python:
# vim: set ts=4 sts=4 sw=4 et:
# AGORA Another Generator Of Rest Api
# Copyright (c) 2018, 2019 - beg0
#

import sys,os
import unittest

#for d in [os.path.realpath(os.path.join(os.path.dirname(sys.argv[0]), '..')), '.']:
#    sys.path.insert(0,d)

from agora.InternalNode import InternalNode,InternalMethod

class TestInternalNode(unittest.TestCase):
    def test_xtor(self):
        name = "james_bond"
        node = InternalNode(name,None)

        self.assertEqual(node.name, name)
        self.assertEqual(node.parent, None)
        self.assertEqual(node.children, {})
        self.assertEqual(node.param_children,{})
        self.assertEqual(node.methods,[])
        self.assertEqual(node.doc,None)
        self.assertEqual(node.varname,None)

        self.assertFalse(node.is_placeholder())

    def test_xtor_param(self):
        varname = "id"
        name = "${%s}" % varname
        node = InternalNode(name,None)

        self.assertEqual(node.name, name)
        self.assertEqual(node.parent, None)
        self.assertEqual(node.children, {})
        self.assertEqual(node.param_children,{})
        self.assertEqual(node.methods,[])
        self.assertEqual(node.doc,None)
        self.assertEqual(node.varname,varname)

        self.assertTrue(node.is_placeholder())

    def test_add_child(self):
        name1 = "agents"
        name2 = "james_bond"
        root = InternalNode(name1,None)

        self.assertEqual(root.children,{})
        node = root.add_child(name2)

        self.assertIsInstance(node, InternalNode)
        self.assertEqual(node.parent, root)
        self.assertEqual(node.name, name2)

        self.assertEqual(root.children, { name2: node})
        self.assertEqual(root.param_children, {})

        self.assertFalse(node.is_placeholder())

        #test idempotent
        node_dup = root.add_child(name2)
        self.assertEqual(node, node_dup)

    def test_add_child_param(self):
        name1 = "agents"
        varname = "id"
        name2 = "${%s}" % varname
        root = InternalNode(name1,None)

        self.assertEqual(root.param_children,{})
        node = root.add_child(name2)

        self.assertIsInstance(node, InternalNode)
        self.assertEqual(node.parent, root)
        self.assertEqual(node.name, name2)

        self.assertEqual(root.children, {})
        self.assertEqual(root.param_children, { varname: node})

        self.assertTrue(node.is_placeholder())

        #test idempotent
        node_dup = root.add_child(name2)
        self.assertEqual(node, node_dup)


    def test_get_url(self):
        name1 = "agents"
        name2 = "james_bond"
        root = InternalNode(name1,None)

        node = root.add_child(name2)

        self.assertEqual(root.get_url(),name1)
        self.assertEqual(node.get_url(),"%s/%s" % (name1, name2))

    def test_get_url_param(self):
        name1 = "agents"
        varname = "id"
        name2 = "${%s}" % varname
        root = InternalNode(name1,None)

        node = root.add_child(name2)

        self.assertEqual(root.get_url(),name1)
        self.assertEqual(node.get_url(),"%s/%s" % (name1, name2))


    def test_add_method(self):
        name = "james_bond"
        node = InternalNode(name,None)

        self.assertEqual(node.methods,[])

        node.add_method("get")
        self.assertEqual(node.methods,[InternalMethod("GET")])

        #test idempotent
        node.add_method("get")
        self.assertEqual(node.methods,[InternalMethod("GET")])


        node.add_method("put")
        self.assertEqual(node.methods,[InternalMethod("GET"),InternalMethod("PUT")])

    def test_set_doc(self):
        name = "james_bond"
        helpstring="RTFM"
        helpstring_unicode=u"RTFM"
        node = InternalNode(name,None)

        self.assertEqual(node.doc,None)

        node.set_doc(helpstring)

        self.assertEqual(node.doc, helpstring)

        node.set_doc(helpstring_unicode)
        self.assertEqual(node.doc, helpstring_unicode)

        node.set_doc(None)
        self.assertEqual(node.doc,None)

        with self.assertRaisesRegexp(ValueError, "bad type for doc: got int, expected string"):
            node.set_doc(12)

        self.assertEqual(node.doc,None)
