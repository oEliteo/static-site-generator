import unittest
from re import split

from split_nodes_delimiter import split_nodes_delimiter
from textnode import TextNode


class Test_Split_Nodes(unittest.TestCase):

    def test_pair(self):
        node = TextNode(
            text="This is a `code` node.", text_type=TextNode.TextType.TEXT, url=None
        )
        new_nodes = split_nodes_delimiter([node], "`", TextNode.TextType.CODE)
        expected_nodes = 3
        expected_text_0 = "This is a "
        expected_text_1 = "code"
        expected_text_2 = " node."
        expected_type_0 = TextNode.TextType.TEXT
        expected_type_1 = TextNode.TextType.CODE
        expected_type_2 = TextNode.TextType.TEXT
        self.assertEqual(expected_nodes, len(new_nodes))
        self.assertEqual(expected_text_0, new_nodes[0].text)
        self.assertEqual(expected_type_0, new_nodes[0].text_type)
        self.assertEqual(expected_text_1, new_nodes[1].text)
        self.assertEqual(expected_type_1, new_nodes[1].text_type)
        self.assertEqual(expected_text_2, new_nodes[2].text)
        self.assertEqual(expected_type_2, new_nodes[2].text_type)

    def test_unmatched(self):
        node = TextNode(
            text="This is a `mismatched node.",
            text_type=TextNode.TextType.TEXT,
            url=None,
        )
        with self.assertRaises(Exception) as err:
            split_nodes_delimiter([node], "`", TextNode.TextType.CODE)

        self.assertEqual(
            str(err.exception), "Invalid markdown, missing closing delimiter."
        )

    def test_empty_with_delimiter(self):
        node = TextNode("****", TextNode.TextType.TEXT, None)
        node2 = TextNode("Hello, World!", TextNode.TextType.TEXT, None)

        expected_text_0 = "Hello, World!"
        expected_type_0 = TextNode.TextType.TEXT

        new_nodes = split_nodes_delimiter([node], "**", TextNode.TextType.BOLD)
        self.assertEqual([], new_nodes)

        new_nodes = split_nodes_delimiter([node, node2], "**", TextNode.TextType.BOLD)

        self.assertEqual(expected_text_0, new_nodes[0].text)
        self.assertEqual(expected_type_0, new_nodes[0].text_type)

    def test_already_converted(self):
        node = TextNode("**Hello**, World!", TextNode.TextType.TEXT, None)
        node2 = TextNode("Already Bold", TextNode.TextType.BOLD, None)
        node3 = TextNode("Already Italic", TextNode.TextType.ITALIC, None)

        new_nodes = split_nodes_delimiter(
            [node, node2, node3], "**", TextNode.TextType.BOLD
        )

        self.assertEqual(4, len(new_nodes))
        self.assertEqual(TextNode.TextType.BOLD, new_nodes[0].text_type)
        self.assertEqual(TextNode.TextType.TEXT, new_nodes[1].text_type)
        self.assertEqual(TextNode.TextType.BOLD, new_nodes[2].text_type)
        self.assertEqual(TextNode.TextType.ITALIC, new_nodes[3].text_type)

        self.assertEqual("Hello", new_nodes[0].text)
        self.assertEqual(", World!", new_nodes[1].text)
        self.assertEqual("Already Bold", new_nodes[2].text)
        self.assertEqual("Already Italic", new_nodes[3].text)
