import unittest

from htmlnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode(tag="a", value="boot.dev", props={"href": "https://boot.dev"})
        self.assertEqual(node.to_html(), '<a href="https://boot.dev">boot.dev</a>')

    def test_leav_to_html_h1(self):
        node = LeafNode(tag="h1", value="This is a h1 tag with this text")
        self.assertEqual(node.to_html(), "<h1>This is a h1 tag with this text</h1>")
