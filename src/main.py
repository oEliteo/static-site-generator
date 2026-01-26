from textnode import TextNode


def main():
    test_node = TextNode(
        "This is some anchor text", TextNode.TextType.LINK, "https://www.boot.dev"
    )
    print(test_node)
    return


main()
