from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):

    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            strings = node.text.split(delimiter)
            if len(strings) % 2 == 0:
                raise Exception("Invalid markdown, missing closing delimiter.")

            for i in range(len(strings)):
                if strings[i] == "":
                    continue
                if i % 2 == 0:
                    new_nodes.append(TextNode(strings[i], TextType.TEXT))
                else:
                    new_nodes.append(TextNode(strings[i], text_type))
        else:
            new_nodes.append(node)

    return new_nodes
