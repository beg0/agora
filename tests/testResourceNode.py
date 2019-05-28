# vim: set syntax=python:
# vim: set ts=4 sts=4 sw=4 et:
# AGORA Another Generator Of Rest Api
# Copyright (c) 2018, 2019 - beg0
#

import sys,os
import types
import unittest

for d in [os.path.realpath(os.path.join(os.path.dirname(sys.argv[0]), '..'))]:
    sys.path.insert(0,d)

from agora.ResourceNode import *
from agora.InternalNode import *

class TestResourceNode(unittest.TestCase):
    BASE_URL="http://example.com"
    def setUp(self):
        self.root_intenal = root = InternalNode(TestResourceNode.BASE_URL,None)
        child1=root.add_child("child1")
        param_child1 = root.add_child('${param1}')
        param_child2 = root.add_child('${param2}')

        child2=child1.add_child("child2")
        param_child3 = child1.add_child('${param3}')

        child3=root.add_child("child3")

        child1.add_method("get")
        child1.add_method("post")
        child2.add_method("put")
        child3.add_method("delete")


    def test_attribute_creations(self):
        root = RootResourceNode(self.root_intenal)

        child1=root.child1
        child2=root.child1.child2

        self.assertIs(child1,root.child1, "don't recreate attribute")
        self.assertIs(child2,root.child1.child2,"don't recreate attribute")

        self.assertIsNot(child1,child2)

        self.assertIsInstance(child1, ResourceNode)
        self.assertIsInstance(child2, ResourceNode)

        with self.assertRaises(AttributeError):
            root.not_a_child

    def test_call_no_arguments(self):
        root = RootResourceNode(self.root_intenal)

        self.assertIs(root(),root, "call with no args return same object")
        self.assertIs(root.child1(),root.child1,"call with no args return same object")
        self.assertIs(root.child1.child2(),root.child1.child2,"call with no args return same object")

    def test_param_creation_by_kwargs(self):
        root = RootResourceNode(self.root_intenal)

        param_child1 = root(param1="arg_first_param")
        param_child2 = root(param2="arg_second_param")

        self.assertIsInstance(param_child1, ParamResourceNode)
        self.assertIsInstance(param_child2, ParamResourceNode)

        self.assertIs(root(param1="arg_first_param"),param_child1, "don't recreate param")
        self.assertNotEqual(root(param1="another_arg_first_param"),param_child1, "different args give differents nodes")

        self.assertNotEqual(param_child1, param_child2)


        with self.assertRaisesRegexp(TypeError,"No such parameter"):
            root(spoon="there_is_no_spoon")

        with self.assertRaisesRegexp(TypeError,"Too many named arguments.*"):
            root(param1="arg_first_param",param2="arg_second_param")


    def test_param_creation_by_list(self):
        root = RootResourceNode(self.root_intenal)

        with self.assertRaisesRegexp(TypeError,"Can't deduce parameter name:.*"):
            root("bad arg")

        with self.assertRaisesRegexp(TypeError,"There is no parameter for this URL"):
            root.child3("bad arg")

        param_child3 = root.child1("arg_third_param")
        self.assertIsInstance(param_child3, ParamResourceNode)

        self.assertEqual(param_child3, root.child1(param3="arg_third_param"),"creation by list == creation by kw")

        with self.assertRaisesRegexp(TypeError,"Too many positional argument, except at max one"):
            root.child1("arg_third_param","arg_third_param_bis")


    def test_call_with_both_list_and_kwargs(self):
        root = RootResourceNode(self.root_intenal)
        with self.assertRaisesRegexp(TypeError,"Except at max one positional argument or one named argument.*"):
            root("arg_first_param",param1="arg_first_param")


    def test_url(self):
        root = RootResourceNode(self.root_intenal)
        self.assertEqual(root.child1.url, TestResourceNode.BASE_URL+"/child1")
        self.assertEqual(root.child1.child2.url, TestResourceNode.BASE_URL+"/child1/child2")

    def test_set_base_url(self):
        root = RootResourceNode(self.root_intenal)
        new_base_url="http://127.0.0.1"
        root.set_base_url(new_base_url)
        self.assertEqual(root.child1.url, new_base_url+"/child1")
        self.assertEqual(root.child1.child2.url, new_base_url+"/child1/child2")
        self.assertEqual(root.child1("arg_third_param").url, new_base_url+"/child1/arg_third_param")

    def test_http_methods(self):
        root = RootResourceNode(self.root_intenal)

        child1=root.child1
        child2=root.child1.child2

        self.assertIsInstance(child1.get,types.MethodType)
        self.assertIsInstance(child1.post,types.MethodType)

        with self.assertRaises(AttributeError):
            isinstance(child1.put, types.MethodType)

        self.assertIsInstance(child2.put,types.MethodType)

    def test_verb_translator(self):
        root = RootResourceNode(self.root_intenal)

        child1=root.child1

        self.assertTrue(hasattr(child1,"get"), "if no translator, we have lowercase verb name")
        self.assertFalse(hasattr(child1,"TEG"), "if no translator, we don't have reversed verb name")


        def reverse_verb(method):
            return method.verb[::-1]

        root_reverse = RootResourceNode(self.root_intenal, verb_translator=reverse_verb)

        child1_reverse=root_reverse.child1

        self.assertTrue(hasattr(child1_reverse,"TEG"), "if we have translator, we have reversed verb name")
        self.assertFalse(hasattr(child1_reverse,"get"), "if we have translator, we don't have lowercase verb name")

