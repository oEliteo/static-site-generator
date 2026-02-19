import re

from textnode import TextNode


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

        if node.text_type == TextNode.TextType.TEXT:
            matches = extract_markdown_images(split)
            for match in matches:
                split = split.split(f"![{match[0]}]({match[1]})", 1)

                if split[0] == "":
                    split = split[1]
                    new_nodes.append(
                        TextNode(
                            text=match[0],
                            text_type=TextNode.TextType.IMAGE,
                            url=match[1],
                        )
                    )

                else:
                    new_nodes.append(
                        TextNode(
                            text=split[0], text_type=TextNode.TextType.TEXT, url=None
                        )
                    )

                    new_nodes.append(
                        TextNode(
                            text=match[0],
                            text_type=TextNode.TextType.IMAGE,
                            url=match[1],
                        )
                    )
                    split = split[1]

            if split:

                new_nodes.append(
                    TextNode(text=split, text_type=TextNode.TextType.TEXT, url=None)
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

        if node.text_type == TextNode.TextType.TEXT:
            matches = extract_markdown_links(split)
            for match in matches:
                split = split.split(f"[{match[0]}]({match[1]})", 1)

                if split[0] == "":
                    split = split[1]
                    new_nodes.append(
                        TextNode(
                            text=match[0],
                            text_type=TextNode.TextType.LINK,
                            url=match[1],
                        )
                    )

                else:
                    new_nodes.append(
                        TextNode(
                            text=split[0], text_type=TextNode.TextType.TEXT, url=None
                        )
                    )

                    new_nodes.append(
                        TextNode(
                            text=match[0],
                            text_type=TextNode.TextType.LINK,
                            url=match[1],
                        )
                    )
                    split = split[1]

            if split:
                new_nodes.append(
                    TextNode(text=split, text_type=TextNode.TextType.TEXT, url=None)
                )

        else:
            new_nodes.append(node)
            continue

    return new_nodes
