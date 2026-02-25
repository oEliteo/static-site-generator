import re

from split_nodes_delimiter import split_nodes_delimiter
from textnode import TextNode, TextType


def extract_title(md):
    lines = md.split("\n")

    for line in lines:
        if line.startswith("# "):
            return line[2::]

    raise Exception("h1 not found in provided markdown")


def extract_markdown_images(text):
    matches = re.findall(r"!\[([^[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:

        if node.text == "":
            continue

        split = node.text

        if node.text_type == TextType.TEXT:
            matches = extract_markdown_images(split)
            for match in matches:
                split = split.split(f"![{match[0]}]({match[1]})", 1)

                if split[0] == "":
                    split = split[1]
                    new_nodes.append(
                        TextNode(
                            text=match[0],
                            text_type=TextType.IMAGE,
                            url=match[1],
                        )
                    )

                else:
                    new_nodes.append(
                        TextNode(text=split[0], text_type=TextType.TEXT, url=None)
                    )

                    new_nodes.append(
                        TextNode(
                            text=match[0],
                            text_type=TextType.IMAGE,
                            url=match[1],
                        )
                    )
                    split = split[1]

            if split:

                new_nodes.append(
                    TextNode(text=split, text_type=TextType.TEXT, url=None)
                )

        else:
            new_nodes.append(node)
            continue

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:

        if node.text == "":
            continue

        split = node.text

        if node.text_type == TextType.TEXT:
            matches = extract_markdown_links(split)
            for match in matches:
                split = split.split(f"[{match[0]}]({match[1]})", 1)

                if split[0] == "":
                    split = split[1]
                    new_nodes.append(
                        TextNode(
                            text=match[0],
                            text_type=TextType.LINK,
                            url=match[1],
                        )
                    )

                else:
                    new_nodes.append(
                        TextNode(text=split[0], text_type=TextType.TEXT, url=None)
                    )

                    new_nodes.append(
                        TextNode(
                            text=match[0],
                            text_type=TextType.LINK,
                            url=match[1],
                        )
                    )
                    split = split[1]

            if split:
                new_nodes.append(
                    TextNode(text=split, text_type=TextType.TEXT, url=None)
                )

        else:
            new_nodes.append(node)
            continue

    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]

    nodes = split_nodes_image(nodes)

    nodes = split_nodes_link(nodes)

    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)

    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)

    return nodes


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    processed_blocks = []
    for block in blocks:
        temp = block.strip(" \t\n")
        if temp:
            processed_blocks.append(temp)

    return processed_blocks
