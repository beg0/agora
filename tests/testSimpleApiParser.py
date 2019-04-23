# vim: set syntax=python:
# vim: set ts=4 sts=4 sw=4 et:
# AGORA Another Generator Of Rest Api
# Copyright (c) 2018, 2019 - beg0
#

import unittest
from unittest.util import safe_repr
import sys, os.path

from agora.SimpleApiParser import SimpleApiParser
from agora.InternalNode import InternalNode, InternalMethod


class TestSimpleParser(unittest.TestCase):
    lorem_ipsum =  """ consequatur aut est tempora reiciendis laudantium minima sapiente est ipsa suscipit culpa aperiam illum est  """
    lorem_ipsum2 =  """ non quod minima sed pariatur voluptatem quia et fugit est rem qui autem corrupti ducimus """
    resources=[
            { "url": "/", "doc": lorem_ipsum },
            { "url": "/message/${author}/", "method": "get", "doc":lorem_ipsum2 },
            { "url": "/user/", "method": "get" },
            { "url": "/user/", "method": "post" },
            { "url": "/user/avatar", "method": "get" },
            { "url": "/user/avatar", "method": "put" },
            { "url": "/user/${username}", "method": "get" },
            { "url": "/user/${username}", "method": "put" },
            { "url": "/user/${username}", "method": "delete" },
            { "url": "/user/${username}/friend", "method": "get" },
            { "url": "/user/${username}/friend", "method": "post" },
            { "url": "/user/${username}/friend/${friendname}", "method": "get" },
            { "url": "/user/${username}/friend/${friendname}", "method": "delete" }
            ]
    def assertEmpty(self, expr, msg=None):
        """ Check that an sequence  is empty (e.g. a length of 0) """
        try:
            l = len(expr)
        except (TypeError, NotImplementedError):
            msg = self._formatMessage(msg, '%s has no length.    Non-sequence?' % (type(expr).__name__))
            raise self.failureException(msg)

        if l != 0:
            msg = self._formatMessage(msg, "%s is not empty" % safe_repr(expr))
            raise self.failureException(msg)

    def assertDictHasKey(self, d, expectedKeys, msg=None):
        self.assertListEqual(sorted(d.keys()),sorted(expectedKeys),msg=msg)

    def setUp(self):
        self.parser = SimpleApiParser(TestSimpleParser.resources)


    def test_children(self):
        root = self.parser.parse()
        self.assertIsInstance(root, InternalNode)

        self.assertDictHasKey(root.children, ["message","user"])
        self.assertEmpty(root.param_children)

        # node "message"
        messageNode = root.children["message"]

        self.assertIsInstance(messageNode, InternalNode)

        self.assertEmpty(messageNode.children)
        self.assertDictHasKey(messageNode.param_children,["author"])

        # node "author"
        authorNode = messageNode.param_children["author"]

        self.assertIsInstance(authorNode, InternalNode)

        self.assertEmpty(authorNode.children)
        self.assertEmpty(authorNode.param_children)


        # node "user"
        userNode = root.children["user"]

        self.assertIsInstance(userNode, InternalNode)

        self.assertDictHasKey(userNode.children, ["avatar"])
        self.assertDictHasKey(userNode.param_children, ["username"])

        # node "avatar"
        avatarNode = userNode.children["avatar"]

        self.assertIsInstance(avatarNode, InternalNode)

        self.assertEmpty(avatarNode.children)
        self.assertEmpty(avatarNode.param_children)

        # node "username"
        usernameNode = userNode.param_children["username"]

        self.assertIsInstance(usernameNode, InternalNode)

        self.assertDictHasKey(usernameNode.children, ["friend"])
        self.assertEmpty(usernameNode.param_children)

        # node "friend"
        friendNode = usernameNode.children["friend"]

        self.assertIsInstance(friendNode, InternalNode)

        self.assertEmpty(friendNode.children)
        self.assertDictHasKey(friendNode.param_children, ["friendname"])

        # node "friendname"
        friendnameNode = friendNode.param_children["friendname"]
        self.assertIsInstance(friendnameNode, InternalNode)

        self.assertEmpty(friendnameNode.children)
        self.assertEmpty(friendnameNode.param_children)


    def test_methods(self):
        root = self.parser.parse()
        self.assertIsInstance(root, InternalNode)

        messageNode = root.children["message"]
        authorNode = messageNode.param_children["author"]
        userNode = root.children["user"]
        avatarNode = userNode.children["avatar"]
        usernameNode = userNode.param_children["username"]
        friendNode = usernameNode.children["friend"]
        friendnameNode = friendNode.param_children["friendname"]

        self.assertEqual(root.methods, [])
        self.assertEqual(messageNode.methods, [])
        self.assertEqual(authorNode.methods, [InternalMethod("GET")])
        self.assertEqual(userNode.methods, [InternalMethod("GET"), InternalMethod("POST")])
        self.assertEqual(avatarNode.methods, [InternalMethod("GET"),InternalMethod("PUT")])
        self.assertEqual(usernameNode.methods, [InternalMethod("DELETE"), InternalMethod("GET"),InternalMethod("PUT")])
        self.assertEqual(friendNode.methods, [InternalMethod("GET"),InternalMethod("POST")])
        self.assertEqual(friendnameNode.methods, [InternalMethod("DELETE"), InternalMethod("GET")])

    def test_names(self):
        root = self.parser.parse()
        self.assertIsInstance(root, InternalNode)

        messageNode = root.children["message"]
        authorNode = messageNode.param_children["author"]
        userNode = root.children["user"]
        avatarNode = userNode.children["avatar"]
        usernameNode = userNode.param_children["username"]
        friendNode = usernameNode.children["friend"]
        friendnameNode = friendNode.param_children["friendname"]

        self.assertEqual(root.name, "")
        self.assertEqual(messageNode.name, "message")
        self.assertEqual(authorNode.name, "${author}")
        self.assertEqual(userNode.name, "user")
        self.assertEqual(avatarNode.name, "avatar")
        self.assertEqual(usernameNode.name, "${username}")
        self.assertEqual(friendNode.name, "friend")
        self.assertEqual(friendnameNode.name, "${friendname}")

    def test_varname(self):
        root = self.parser.parse()
        self.assertIsInstance(root, InternalNode)

        messageNode = root.children["message"]
        authorNode = messageNode.param_children["author"]
        userNode = root.children["user"]
        avatarNode = userNode.children["avatar"]
        usernameNode = userNode.param_children["username"]
        friendNode = usernameNode.children["friend"]
        friendnameNode = friendNode.param_children["friendname"]

        self.assertEqual(root.varname, None)
        self.assertEqual(messageNode.varname, None)
        self.assertEqual(authorNode.varname, "author")
        self.assertEqual(userNode.varname, None)
        self.assertEqual(avatarNode.varname, None)
        self.assertEqual(usernameNode.varname, "username")
        self.assertEqual(friendNode.varname, None)
        self.assertEqual(friendnameNode.varname, "friendname")

    def test_parent(self):
        root = self.parser.parse()
        self.assertIsInstance(root, InternalNode)

        messageNode = root.children["message"]
        authorNode = messageNode.param_children["author"]
        userNode = root.children["user"]
        avatarNode = userNode.children["avatar"]
        usernameNode = userNode.param_children["username"]
        friendNode = usernameNode.children["friend"]
        friendnameNode = friendNode.param_children["friendname"]

        self.assertEqual(root.parent, None)
        self.assertEqual(messageNode.parent, root)
        self.assertEqual(authorNode.parent, messageNode)
        self.assertEqual(userNode.parent, root)
        self.assertEqual(avatarNode.parent, userNode)
        self.assertEqual(usernameNode.parent, userNode)
        self.assertEqual(friendNode.parent, usernameNode)
        self.assertEqual(friendnameNode.parent, friendNode)

    def test_url(self):
        root = self.parser.parse()
        self.assertIsInstance(root, InternalNode)

        messageNode = root.children["message"]
        authorNode = messageNode.param_children["author"]
        userNode = root.children["user"]
        avatarNode = userNode.children["avatar"]
        usernameNode = userNode.param_children["username"]
        friendNode = usernameNode.children["friend"]
        friendnameNode = friendNode.param_children["friendname"]

        self.assertEqual(root.get_url(), "")
        self.assertEqual(messageNode.get_url(), "/message")
        self.assertEqual(authorNode.get_url(), "/message/${author}")
        self.assertEqual(userNode.get_url(), "/user")
        self.assertEqual(avatarNode.get_url(), "/user/avatar")
        self.assertEqual(usernameNode.get_url(), "/user/${username}")
        self.assertEqual(friendNode.get_url(), "/user/${username}/friend")
        self.assertEqual(friendnameNode.get_url(), "/user/${username}/friend/${friendname}")

    def test_doc(self):
        root = self.parser.parse()
        self.assertIsInstance(root, InternalNode)

        messageNode = root.children["message"]
        authorNode = messageNode.param_children["author"]
        userNode = root.children["user"]
        avatarNode = userNode.children["avatar"]
        usernameNode = userNode.param_children["username"]
        friendNode = usernameNode.children["friend"]
        friendnameNode = friendNode.param_children["friendname"]

        self.assertEqual(root.doc, self.lorem_ipsum)
        self.assertEqual(messageNode.doc, None)
        self.assertEqual(authorNode.doc, self.lorem_ipsum2)
        self.assertEqual(userNode.doc, None)
        self.assertEqual(avatarNode.doc, None)
        self.assertEqual(usernameNode.doc, None)
        self.assertEqual(friendNode.doc, None)
        self.assertEqual(friendnameNode.doc, None)


    def test_empty_resource(self):
        root = SimpleApiParser([]).parse()

        self.assertIsInstance(root, InternalNode)
        self.assertEqual(root.get_url(), "")
        self.assertEqual(len(root.children),0)
        self.assertEqual(len(root.param_children),0)

    def test_wrong_tree(self):
        with self.assertRaisesRegexp(AssertionError,"must be a list of resource, got .*"):
            SimpleApiParser(666)

        with self.assertRaises(AssertionError):
            bad_resource=[666]
            parser = SimpleApiParser(bad_resource)

        with self.assertRaises(AssertionError):
            bad_resource=[{"foo":"bar"}]
            parser = SimpleApiParser(bad_resource)

        with self.assertRaises(AssertionError):
            bad_resource=[
                    {"url":""}
            ]
            parser = SimpleApiParser(bad_resource)

