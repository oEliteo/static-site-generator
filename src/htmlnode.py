from textnode import TextNode


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

        case TextNode.TextType.TEXT:
            return LeafNode(tag=None, value=text_node.text)

        case TextNode.TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)

        case TextNode.TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)

        case TextNode.TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)

        case TextNode.TextType.LINK:
            return LeafNode(
                tag="a", value=text_node.text, props={"href": f"{text_node.url}"}
            )

        case TextNode.TextType.IMAGE:
            return LeafNode(
                tag="img",
                value="",
                props={"src": f"{text_node.url}", "alt": f"{text_node.text}"},
            )

        case _:
            raise ValueError("TextNode must have a valid TextType value.")
