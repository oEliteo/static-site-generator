import unittest

from htmlnode import LeafNode, ParentNode


class TestParentNode(unittest.TestCase):

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_no_children(self):
        parent_node = ParentNode("div", [])
        with self.assertRaises(ValueError) as err:
            parent_node.to_html()

        self.assertEqual(
            str(err.exception), "All parent nodes must contain at least one child node."
        )

    def test_to_html_no_tag(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])

        with self.assertRaises(ValueError) as err:
            parent_node.to_html()

        self.assertEqual(str(err.exception), "All parent nodes must contain a tag.")

    def test_to_html_empty_tag(self):
        child_node = LeafNode("div", "child")
        parent_node = ParentNode("", [child_node])

        with self.assertRaises(ValueError) as err:
            parent_node.to_html()

        self.assertEqual(str(err.exception), "All parent nodes must contain a tag.")
