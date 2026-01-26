import unittest

from htmlnode import HTMLNode


class TestHtmlNode(unittest.TestCase):

    def test_props_to_html_1(self):
        node = HTMLNode(
            "a", "boot.dev", [], {"href": "https://boot.dev/", "target": "_blank"}
        )

        self.assertEqual(
            node.props_to_html(), ' href="https://boot.dev/" target="_blank"'
        )

    def test_props_to_html_no_props(self):
        node = HTMLNode("a", "boot.dev", [], {})

        self.assertEqual(node.props_to_html(), "")

    def test_htmlnode_children(self):
        child = HTMLNode(
            "p", "boot.dev is a great platform for learning to code.", [], {}
        )
        parent = HTMLNode("a", "boot.dev", [child], {})

        self.assertEqual(parent.children[0], child)

    def test_repr(self):
        node = HTMLNode("a", "boot.dev", [], {})
        expected = (
            f"Tag: {node.tag}\n"
            + f"{node.value}\n"
            + f"{node.children}\n"
            + f"{node.props}\n"
        )
        self.assertEqual(node.__repr__(), expected)
