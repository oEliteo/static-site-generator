import unittest

from extract_markdown import (
    extract_markdown_images,
    extract_markdown_links,
    extract_title,
    markdown_to_blocks,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
from htmlnode import text_node_to_html_node
from textnode import TextNode, TextType


class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
        matches = extract_markdown_images("This is text with a [link](https://boot.dev")
        self.assertListEqual([], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links("This is text with a [link](https://boot.dev)")
        self.assertListEqual([("link", "https://boot.dev")], matches)
        matches = extract_markdown_links(
            "this is text with an ![image](https://imgur.com/abcdefg123)"
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_multi_image(self):
        matches = extract_markdown_images(
            "this is text with several ![images](https://i.imgur.com/zjjcJKZ.png), ![another image](https://i.imgur.com/zjjcJKZ.png), ![one more](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(
            [
                ("images", "https://i.imgur.com/zjjcJKZ.png"),
                ("another image", "https://i.imgur.com/zjjcJKZ.png"),
                ("one more", "https://i.imgur.com/zjjcJKZ.png"),
            ],
            matches,
        )

    def test_extract_markdown_multi_link(self):
        matches = extract_markdown_links(
            "this is text with several [links](https://i.imgur.com/zjjcJKZ.png), [another link](https://i.imgur.com/zjjcJKZ.png), [one more](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(
            [
                ("links", "https://i.imgur.com/zjjcJKZ.png"),
                ("another link", "https://i.imgur.com/zjjcJKZ.png"),
                ("one more", "https://i.imgur.com/zjjcJKZ.png"),
            ],
            matches,
        )

    def test_different_types_extract_markdown_images(self):
        matches = extract_markdown_images(
            "this is text with different kinds of markdown. ![image](https://i.imgur.com/zjjcJKZ.png), [link](https://i.imgur.com/zjjcJKZ.png), ![another image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(
            [
                ("image", "https://i.imgur.com/zjjcJKZ.png"),
                ("another image", "https://i.imgur.com/zjjcJKZ.png"),
            ],
            matches,
        )

    def test_different_types_extract_markdown_links(self):
        matches = extract_markdown_links(
            "this is text with different kinds of markdown. ![image](https://i.imgur.com/zjjcJKZ.png), [link](https://i.imgur.com/zjjcJKZ.png), ![another image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(
            [("link", "https://i.imgur.com/zjjcJKZ.png")],
            matches,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image",
                    TextType.IMAGE,
                    "https://i.imgur.com/3elNhQu.png",
                ),
            ],
            new_nodes,
        )

        node = TextNode(
            "This is text with an ![image](https://some.image.png) and a link [link](https://some.link.com)",
            TextType.TEXT,
        )
        node2 = TextNode(
            "![image](https://some.image.png)[link](https://some.link.com)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_image([node, node2])

        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode(
                    "image",
                    TextType.IMAGE,
                    url="https://some.image.png",
                ),
                TextNode(
                    " and a link [link](https://some.link.com)",
                    TextType.TEXT,
                ),
                TextNode(
                    "image",
                    TextType.IMAGE,
                    url="https://some.image.png",
                ),
                TextNode("[link](https://some.link.com)", TextType.TEXT),
            ],
            new_nodes,
        )

        node = TextNode("This node contains nothing of importance", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This node contains nothing of importance", TextType.TEXT),
            ],
            new_nodes,
        )

        node = TextNode("This is a bold node", TextType.BOLD)

        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [TextNode("This is a bold node", TextType.BOLD)], new_nodes
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link",
                    TextType.LINK,
                    "https://i.imgur.com/3elNhQu.png",
                ),
            ],
            new_nodes,
        )

        node = TextNode(
            "This is text with a ![image](https://some.image.png) and a [link](https://some.link.com)",
            TextType.TEXT,
        )
        node2 = TextNode(
            "![image](https://some.image.png)[link](https://some.link.com)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link([node, node2])

        self.assertListEqual(
            [
                TextNode(
                    "This is text with a ![image](https://some.image.png) and a ",
                    TextType.TEXT,
                ),
                TextNode("link", TextType.LINK, "https://some.link.com"),
                TextNode("![image](https://some.image.png)", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://some.link.com"),
            ],
            new_nodes,
        )

        node = TextNode("This node contains nothing of importance", TextType.TEXT)

        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [TextNode("This node contains nothing of importance", TextType.TEXT)],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "obi wan image",
                TextType.IMAGE,
                "https://i.imgur.com/fJRm4Vk.jpeg",
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]

        nodes = text_to_textnodes(text)

        self.assertListEqual(nodes, expected)

        text = ""

        expected = []

        nodes = text_to_textnodes(text)

        self.assertListEqual(nodes, expected)

        text = "This is plain text only."

        expected = [TextNode("This is plain text only.", TextType.TEXT)]

        nodes = text_to_textnodes(text)

        self.assertListEqual(nodes, expected)

        text = "**bold**"

        expected = [TextNode("bold", TextType.BOLD)]

        nodes = text_to_textnodes(text)

        self.assertListEqual(nodes, expected)

        text = "**bold****morebold**_italic__moreitalic_`code``morecode`"

        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode("morebold", TextType.BOLD),
            TextNode("italic", TextType.ITALIC),
            TextNode("moreitalic", TextType.ITALIC),
            TextNode("code", TextType.CODE),
            TextNode("morecode", TextType.CODE),
        ]

        nodes = text_to_textnodes(text)

        self.assertListEqual(expected, nodes)

        text = "![image](https://some.image.png)**bold**[link](https://some.link.com) some plain text and `code`"

        expected = [
            TextNode("image", TextType.IMAGE, "https://some.image.png"),
            TextNode("bold", TextType.BOLD),
            TextNode("link", TextType.LINK, "https://some.link.com"),
            TextNode(" some plain text and ", TextType.TEXT),
            TextNode("code", TextType.CODE),
        ]

        nodes = text_to_textnodes(text)

        self.assertListEqual(expected, nodes)

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_extract_title(self):
        md = "# Hello\nThis is markdown"
        exp = "Hello"
        title = extract_title(md)

        self.assertEqual(title, exp)
        md = "There is no h1 in here"

        with self.assertRaises(Exception) as err:
            title = extract_title(md)

        self.assertEqual(str(err.exception), "h1 not found in provided markdown")
