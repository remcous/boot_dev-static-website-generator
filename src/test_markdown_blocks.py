import unittest
from markdown_blocks import (
    markdown_to_blocks,
    block_to_block_type,
    block_type_paragraph,
    block_type_heading,
    block_type_code,
    block_type_quote,
    block_type_unordered_list,
    block_type_ordered_list,
    paragraph_block_to_html,
    heading_block_to_html,
    quote_block_to_html,
    code_block_to_html,
    unordered_list_to_html,
    ordered_list_to_html,
    markdown_to_html_node
)

from htmlnode import LeafNode, ParentNode

class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        text = """This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items"""
        expected = [
            """This is **bolded** paragraph""",
            """This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line""",
            """* This is a list
* with items""",
            ]
        self.assertEqual(markdown_to_blocks(text), expected)
        
    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )
        
    def test_block_type_heading1(self):
        block = "# Heading 1"
        expected = block_type_heading
        self.assertEqual(block_to_block_type(block), expected)
    
    def test_block_type_heading6(self):
        block = "###### Heading 6"
        expected = block_type_heading
        self.assertEqual(block_to_block_type(block), expected)
    
    def test_block_type_heading7(self):
        # no such thing as heading 7
        block = "####### Heading 7"
        expected = block_type_paragraph
        self.assertEqual(block_to_block_type(block), expected)
        
    def test_block_type_code1(self):
        block = "```print(hello world)```"
        expected = block_type_code
        self.assertEqual(block_to_block_type(block), expected)
        
    def test_block_type_code2(self):
        block = "``print(hello world)```"
        expected = block_type_paragraph
        self.assertEqual(block_to_block_type(block), expected)
        
    def test_block_type_code3(self):
        block = "```print(hello world)``"
        expected = block_type_paragraph
        self.assertEqual(block_to_block_type(block), expected)
        
    def test_block_type_quote1(self):
        block = """> Quote line 1
> Quote line 2
> Quote line 3"""
        expected = block_type_quote
        self.assertEqual(block_to_block_type(block), expected)
        
    def test_block_type_quote2(self):
        block = """> Quote line 1
Quote line 2
> Quote line 3"""
        expected = block_type_paragraph
        self.assertEqual(block_to_block_type(block), expected)
        
    def test_block_type_ul1(self):
        block = """* item 1
* item 2
* item 3"""
        expected = block_type_unordered_list
        self.assertEqual(block_to_block_type(block), expected)
        
    def test_block_type_ul2(self):
        block = """- item 1
- item 2
- item 3"""
        expected = block_type_unordered_list
        self.assertEqual(block_to_block_type(block), expected)
        
    def test_block_type_ul3(self):
        block = """* item 1
- item 2
* item 3"""
        expected = block_type_unordered_list
        self.assertEqual(block_to_block_type(block), expected)
        
    def test_block_type_ul4(self):
        block = """* item 1
 item 2
* item 3"""
        expected = block_type_paragraph
        self.assertEqual(block_to_block_type(block), expected)
        
    def test_block_type_ol1(self):
        block = """1. item 1
2. item 2
3. item 3"""
        expected = block_type_ordered_list
        self.assertEqual(block_to_block_type(block), expected)
        
    def test_block_type_ol1(self):
        block = """1. item 1
2. item 2
3. item 3"""
        expected = block_type_ordered_list
        self.assertEqual(block_to_block_type(block), expected)
        
    def test_block_type_ol2(self):
        block = """1. item 1
1. item 2
3. item 3"""
        expected = block_type_paragraph
        self.assertEqual(block_to_block_type(block), expected)
        
    def test_block_type_ol3(self):
        block = """1. item 1
2. item 2
item 3"""
        expected = block_type_paragraph
        self.assertEqual(block_to_block_type(block), expected)
        
#     def test_paragraph_block_to_html(self):
#         block = """Here is line 1
# Here is line 2!"""
#         expected = LeafNode("p", """Here is line 1
# Here is line 2!""")
#         self.assertEqual(paragraph_block_to_html(block), expected)
        
    # def test_heading_block_to_html1(self):
    #     block = """# heading level 1"""
    #     expected = LeafNode("h1", "heading level 1")
    #     self.assertEqual(heading_block_to_html(block), expected)
        
    # def test_heading_block_to_html2(self):
    #     block = """###### heading level 6"""
    #     expected = LeafNode("h6", "heading level 6")
    #     self.assertEqual(heading_block_to_html(block), expected)
        
#     def test_quote_block_to_html2(self):
#         block = """>This is a quote
# > so is this"""
#         expected = LeafNode("blockquote", """This is a quote
# so is this""")
#         self.assertEqual(quote_block_to_html(block), expected)

    # def test_code_block_to_html(self):
    #     block = """```This is code```"""
    #     expected = ParentNode("pre", [LeafNode("code", "This is code")])
    #     self.assertEqual(code_block_to_html(block), expected)

#     def test_unordered_list_to_html(self):
#         block = """* item 1
# - item 2"""
#         expected = ParentNode("ul", [
#             LeafNode("li", "item 1"),
#             LeafNode("li", "item 2")
#             ])
#         self.assertEqual(unordered_list_to_html(block), expected)

#     def test_ordered_list_to_html(self):
#         block = """1. item 1
# 2. item 2"""
#         expected = ParentNode("ol", [
#             LeafNode("li", "item 1"),
#             LeafNode("li", "item 2")
#             ])
#         self.assertEqual(unordered_list_to_html(block), expected)

    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with *italic* text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and *more* items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )
    
if __name__ == "__main__":
    unittest.main()