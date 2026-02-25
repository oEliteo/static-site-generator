import os

from block_to_block_type import block_to_block_type
from extract_markdown import extract_title, markdown_to_blocks, text_to_textnodes
from textnode import BlockType, TextNode, TextType


class HTMLNode:

    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):

        return (
            f"Tag: {self.tag}\n"
            + f"{self.value}\n"
            + f"{self.children}\n"
            + f"{self.props}\n"
        )

    def to_html(self):
        raise NotImplementedError("This method is not implemented.")

    def props_to_html(self):
        final_string = ""

        if self.props is None or len(self.props) < 1:
            return ""

        for key in self.props:
            if self.props[key] is not None:
                final_string += " " + key + "=" + f'"{self.props[key]}"'

        return final_string


# Child Class of HTMLNode meant to be a tag / value required node.


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value.")
        if self.tag is None:
            return f"{self.value}"

        else:
            return f"<{self.tag}{super().props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"Tag: {self.tag}\n" + f"{self.value}\n" + f"{self.props}\n"


# Child Class of HTMLNode meant to be a node that requires children, and a tag.


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None) -> None:
        super().__init__(tag=tag, children=children, props=props)
        return None

    def to_html(self) -> str:
        if self.tag is None or len(self.tag) < 1:
            raise ValueError("All parent nodes must contain a tag.")

        if self.children is None or len(self.children) < 1:
            raise ValueError("All parent nodes must contain at least one child node.")

        else:
            output_string = f"<{self.tag}>"
            for i in self.children:
                output_string += i.to_html()

            output_string += f"</{self.tag}>"

        return output_string


def text_node_to_html_node(text_node):

    match text_node.text_type:

        case TextType.TEXT:
            return LeafNode(tag=None, value=text_node.text)

        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)

        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)

        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)

        case TextType.LINK:
            return LeafNode(
                tag="a", value=text_node.text, props={"href": f"{text_node.url}"}
            )

        case TextType.IMAGE:
            return LeafNode(
                tag="img",
                value="",
                props={"src": f"{text_node.url}", "alt": f"{text_node.text}"},
            )

        case _:
            raise ValueError("TextNode must have a valid TextType value.")


def markdown_to_html_node(md):
    blocks = markdown_to_blocks(md)
    main_children = []
    for block in blocks:
        block_type = block_to_block_type(block)

        match block_type:
            case BlockType.PARAGRAPH:
                lines = block.split("\n")
                new_lines = []
                for line in lines:
                    new_lines.append(line.strip("\t\n"))

                new_text = " ".join(new_lines)
                node = ParentNode("p", text_to_children(new_text), None)
                main_children.append(node)
            case BlockType.HEADING:
                heading_num = get_heading_hashtag_count(block)
                block = block[heading_num + 1 : :]
                node = ParentNode(f"h{heading_num}", text_to_children(block), None)
                main_children.append(node)

            case BlockType.CODE:
                block = block[4:-3]
                node = ParentNode(
                    "pre",
                    [
                        ParentNode(
                            "code",
                            [text_node_to_html_node(TextNode(block, TextType.TEXT))],
                            None,
                        )
                    ],
                    None,
                )
                main_children.append(node)
            case BlockType.QUOTE:
                lines = block.split("\n")
                new_lines = []

                for line in lines:
                    new_lines.append(line.lstrip("> "))

                new_text = " ".join(new_lines)

                node = ParentNode(
                    "blockquote",
                    text_to_children(new_text),
                    None,
                )

                main_children.append(node)

            case BlockType.UNORDERED:
                lines = block.split("\n")
                children = []

                for line in lines:
                    children.append(
                        ParentNode(
                            "li",
                            text_to_children(line.lstrip("- ")),
                            None,
                        )
                    )

                node = ParentNode("ul", children, None)
                main_children.append(node)

            case BlockType.ORDERED:
                lines = block.split("\n")
                children = []

                for i in range(len(lines)):
                    children.append(
                        ParentNode(
                            "li", text_to_children(lines[i].split(". ")[1]), None
                        )
                    )
                node = ParentNode("ol", children, None)
                main_children.append(node)

    parent = ParentNode("div", main_children, None)
    return parent


def text_to_children(text):
    nodes = text_to_textnodes(text)

    children = []

    for node in nodes:
        children.append(text_node_to_html_node(node))

    return children


def get_heading_hashtag_count(block):
    if block.startswith("#"):
        hash_count = 0
        for c in block:
            if c == "#":
                hash_count += 1
            elif c == " ":
                break
            if hash_count > 6:
                break

        if (
            1 <= hash_count <= 6
            and len(block) > hash_count
            and block[hash_count] == " "
        ):
            return hash_count


def generate_page(src, template_path, dst, basepath):
    print(f"Generating page from {src} to {dst} using {template_path}.")

    try:
        with open(src, "r") as f:
            md = f.read()

    except FileNotFoundError:
        raise Exception(f"Error: The markdown file '{src}' was not found.")

    try:
        with open(template_path, "r") as f:
            template = f.read()

    except FileNotFoundError:
        raise Exception(f"Error: The template file '{template_path}' was not found.")

    if md and template:
        title = extract_title(md)
        content = markdown_to_html_node(md)
        content = content.to_html()
        html = template.replace("{{ Title }}", title)
        html = html.replace("{{ Content }}", content)
        html = html.replace('href="/', f'href="{basepath}')
        html = html.replace('src="/', f'src="{basepath}')
        dirname = os.path.dirname(dst)
        if dst.endswith(".md"):
            html_path = dst.replace(".md", ".html")
        if dst.endswith(".markdown"):
            html_path = dst.replace(".markdown", ".html")
        os.makedirs(dirname, exist_ok=True)
        with open(html_path, "w") as f:
            f.write(html)


def recurse_generate_pages(src, template_path, dst, basepath):
    items = os.listdir(src)

    with open(template_path, "r") as f:
        template = f.read()

    for item in items:
        from_path = os.path.join(src, item)
        to_path = os.path.join(dst, item)

        if (
            os.path.isfile(from_path)
            and from_path.endswith(".md")
            or from_path.endswith(".markdown")
        ):
            generate_page(from_path, template_path, to_path, basepath)
        else:
            recurse_generate_pages(from_path, template_path, to_path, basepath)
