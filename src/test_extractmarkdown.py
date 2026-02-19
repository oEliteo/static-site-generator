import unittest

from extract_markdown import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
)
from htmlnode import text_node_to_html_node
from textnode import TextNode


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
            TextNode.TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextNode.TextType.TEXT),
                TextNode(
                    "image", TextNode.TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"
                ),
                TextNode(" and another ", TextNode.TextType.TEXT),
                TextNode(
                    "second image",
                    TextNode.TextType.IMAGE,
                    "https://i.imgur.com/3elNhQu.png",
                ),
            ],
            new_nodes,
        )

        node = TextNode(
            "This is text with an ![image](https://some.image.png) and a link [link](https://some.link.com)",
            TextNode.TextType.TEXT,
        )
        node2 = TextNode(
            "![image](https://some.image.png)[link](https://some.link.com)",
            TextNode.TextType.TEXT,
        )

        new_nodes = split_nodes_image([node, node2])

        self.assertListEqual(
            [
                TextNode("This is text with an ", TextNode.TextType.TEXT),
                TextNode(
                    "image",
                    TextNode.TextType.IMAGE,
                    url="https://some.image.png",
                ),
                TextNode(
                    " and a link [link](https://some.link.com)",
                    TextNode.TextType.TEXT,
                ),
                TextNode(
                    "image",
                    TextNode.TextType.IMAGE,
                    url="https://some.image.png",
                ),
                TextNode("[link](https://some.link.com)", TextNode.TextType.TEXT),
            ],
            new_nodes,
        )

        node = TextNode(
            "This node contains nothing of importance", TextNode.TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode(
                    "This node contains nothing of importance", TextNode.TextType.TEXT
                ),
            ],
            new_nodes,
        )

        node = TextNode("This is a bold node", TextNode.TextType.BOLD)

        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [TextNode("This is a bold node", TextNode.TextType.BOLD)], new_nodes
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextNode.TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextNode.TextType.TEXT),
                TextNode(
                    "link", TextNode.TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"
                ),
                TextNode(" and another ", TextNode.TextType.TEXT),
                TextNode(
                    "second link",
                    TextNode.TextType.LINK,
                    "https://i.imgur.com/3elNhQu.png",
                ),
            ],
            new_nodes,
        )

        node = TextNode(
            "This is text with a ![image](https://some.image.png) and a [link](https://some.link.com)",
            TextNode.TextType.TEXT,
        )
        node2 = TextNode(
            "![image](https://some.image.png)[link](https://some.link.com)",
            TextNode.TextType.TEXT,
        )

        new_nodes = split_nodes_link([node, node2])

        self.assertListEqual(
            [
                TextNode(
                    "This is text with a ![image](https://some.image.png) and a ",
                    TextNode.TextType.TEXT,
                ),
                TextNode("link", TextNode.TextType.LINK, "https://some.link.com"),
                TextNode("![image](https://some.image.png)", TextNode.TextType.TEXT),
                TextNode("link", TextNode.TextType.LINK, "https://some.link.com"),
            ],
            new_nodes,
        )

        node = TextNode(
            "This node contains nothing of importance", TextNode.TextType.TEXT
        )

        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode(
                    "This node contains nothing of importance", TextNode.TextType.TEXT
                )
            ],
            new_nodes,
        )
