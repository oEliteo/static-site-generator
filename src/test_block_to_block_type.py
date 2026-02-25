import unittest

from block_to_block_type import block_to_block_type
from extract_markdown import markdown_to_blocks, text_to_textnodes
from textnode import BlockType


class test_block_to_block_type(unittest.TestCase):

    def test_heading(self):
        md = """
# This is a heading.

## This is also a heading.

### A heading.

#### foreheading?

##### fivehead.

###### sixhead.

####### Too much heading.

###Technically but not quite.

"""
        results = []
        expected = [
            BlockType.HEADING,
            BlockType.HEADING,
            BlockType.HEADING,
            BlockType.HEADING,
            BlockType.HEADING,
            BlockType.HEADING,
            BlockType.PARAGRAPH,
            BlockType.PARAGRAPH,
        ]
        for block in markdown_to_blocks(md):
            results.append(block_to_block_type(block))

        self.assertListEqual(results, expected)

    def test_code(self):
        md = """```
This is a code block with
very complicated code that could
save the universe.
```"""
        result = block_to_block_type(md)
        expected = BlockType.CODE

        self.assertEqual(result, expected)

    def test_quote(self):
        md = """> This one guy said this thing.
> It went like this.
> And Ended Like this."""
        result = block_to_block_type(md)
        expected = BlockType.QUOTE

        self.assertEqual(result, expected)

        md = """>This should be a quote
> this should stay a quote.
+ this should break it."""

        result = block_to_block_type(md)
        expected = BlockType.PARAGRAPH

        self.assertEqual(result, expected)

    def test_unordered(self):
        md = """- item1
- item2
- item3"""

        result = block_to_block_type(md)
        expected = BlockType.UNORDERED

        self.assertEqual(result, expected)

        md = """- item1
item 2
- item3"""

        result = block_to_block_type(md)
        expected = BlockType.PARAGRAPH

        self.assertEqual(result, expected)

        md = """This should just become paragraph, lol.
- even with an actual successful check here."""

        result = block_to_block_type(md)
        expected = BlockType.PARAGRAPH

        self.assertEqual(result, expected)

    def test_ordered(self):
        md = """1. item
2. item II
3. item III"""

        result = block_to_block_type(md)
        expected = BlockType.ORDERED

        self.assertEqual(result, expected)

        md = """2. item
1. item
3. item III"""

        result = block_to_block_type(md)
        expected = BlockType.PARAGRAPH

        self.assertEqual(result, expected)

        md = """1. item
2. item
item"""
        result = block_to_block_type(md)
        expected = BlockType.PARAGRAPH

        self.assertEqual(result, expected)

    def test_special(self):
        md = """In the vast and intricate weave of J.R.R. Tolkien's legendarium, amidst heroes of renown and tales of high adventure, there exists a curious anomaly: Tom Bombadil. This peculiar figure, whimsical and unfettered by the weight of Middle-earth's burdens, has long been a point of contention among scholars and enthusiasts. While his character exudes charm and mystery, I, as an ancient **Archmage**, must assert that his inclusion in _The Lord of the Rings_ was, unfortunately, a narrative misstep.

_An unpopular opinion, I know._
"""
        result = block_to_block_type(md)
        expected = BlockType.PARAGRAPH

        self.assertEqual(result, expected)
