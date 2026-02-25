import unittest

from htmlnode import HTMLNode, markdown_to_html_node


class TestHtmlNode(unittest.TestCase):

    def test_props_to_html_1(self):
        node = HTMLNode(
            "a", "boot.dev", [], {"href": "https://boot.dev/", "target": "_blank"}
        )

        self.assertEqual(
            node.props_to_html(), ' href="https://boot.dev/" target="_blank"'
        )

    def test_props_to_html_no_props(self):
        node = HTMLNode("a", "boot.dev", [], {})

        self.assertEqual(node.props_to_html(), "")

    def test_htmlnode_children(self):
        child = HTMLNode(
            "p", "boot.dev is a great platform for learning to code.", [], {}
        )
        parent = HTMLNode("a", "boot.dev", [child], {})

        assert parent.children is not None
        self.assertEqual(parent.children[0], child)

    def test_repr(self):
        node = HTMLNode("a", "boot.dev", [], {})
        expected = (
            f"Tag: {node.tag}\n"
            + f"{node.value}\n"
            + f"{node.children}\n"
            + f"{node.props}\n"
        )
        self.assertEqual(node.__repr__(), expected)

    def test_blocks_to_html_paragraph(self):
        md = """This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_blocks_to_html_heading(self):
        md = """###### H6

##### H5 with _italic_

#### H4 with **bold**

### H3 with `code`

## H2

# H1

######## This should be p.

"""
        node = markdown_to_html_node(md.strip())
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h6>H6</h6><h5>H5 with <i>italic</i></h5><h4>H4 with <b>bold</b></h4><h3>H3 with <code>code</code></h3><h2>H2</h2><h1>H1</h1><p>######## This should be p.</p></div>",
        )

    def test_blocks_to_html_heading_simple(self):
        md = """### This is a h3"""
        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(html, "<div><h3>This is a h3</h3></div>")

    def test_blocks_to_html_code(self):
        md = """```
public void main()
{
  #**Fake bold** comment
  tile = TileID.Campfire;
}
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            """<div><pre><code>public void main()\n{\n  #**Fake bold** comment\n  tile = TileID.Campfire;\n}\n</code></pre></div>""",
        )

    def test_blocks_to_html_quote(self):
        md = """> This was said
> by teddy roosevelt
> or something
"""
        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div><blockquote>This was said by teddy roosevelt or something</blockquote></div>",
        )

    def test_blocks_to_html_unordered(self):
        md = """
- item 1
- item 2
- item 3
- item 4
"""

        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div><ul><li>item 1</li><li>item 2</li><li>item 3</li><li>item 4</li></ul></div>",
        )

    def test_blocks_to_html_ordered(self):
        md = """
1. item 1
2. item 2
3. item 3
4. item 4
"""
        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div><ol><li>item 1</li><li>item 2</li><li>item 3</li><li>item 4</li></ol></div>",
        )
