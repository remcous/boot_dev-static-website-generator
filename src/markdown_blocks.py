import re
from htmlnode import LeafNode, ParentNode
from textnode import text_node_to_html_node
from inline_markdown import text_to_textnodes

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"

def markdown_to_blocks(text):
    blocks = text.split("\n\n")
    return list(map(lambda x: x.strip(), filter(lambda x: x != "", blocks)))

def block_to_block_type(block):
    # check for headings
    if re.search(r"^#{1,6} ", block) is not None:
        return block_type_heading
    
    # check for code blocks
    if re.search(f"^```.*```$", block) is not None:
        return block_type_code
    
    lines = block.split('\n')
    
    # check for quotes
    if all(list(map(lambda line: line[0] == ">", lines))):
        return block_type_quote
    
    # check for unordered list
    if all(list(map(lambda line: line[:2] in ["* ", "- "], lines))):
        return block_type_unordered_list
    
    # check for ordered list
    ordered_list_valid = True
    
    for i,line in enumerate(lines):
        line_tag = f"{i+1}."
        if line[:len(line_tag)] != line_tag:
            ordered_list_valid = False
            break
        
    if ordered_list_valid:
        return block_type_ordered_list
    
    return block_type_paragraph

def paragraph_block_to_html(block):
    block = " ".join(block.split("\n"))
    return ParentNode("p", [text_node_to_html_node(x) for x in text_to_textnodes(block)])

def heading_block_to_html(block):
    block = " ".join(block.split("\n"))
    heading_pounds = block.split(" ")[0]
    heading_level = len(heading_pounds)
    return ParentNode(f"h{heading_level}", [text_node_to_html_node(x) for x in text_to_textnodes(block[heading_level+1:])])

def quote_block_to_html(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        new_lines.append(line[1:].lstrip())
    block = " ".join(new_lines)
    return ParentNode("blockquote", [text_node_to_html_node(x) for x in text_to_textnodes(block)])
                    
def code_block_to_html(block):
    block = " ".join(block.split("\n"))
    return ParentNode("pre", children=[
        ParentNode("code", [text_node_to_html_node(x) for x in text_to_textnodes(block[3:-3])])
    ])
    
def unordered_list_to_html(block):
    root_node = ParentNode("ul", children=[])
    for line in block.split("\n"):
        child_node = ParentNode("li", children=[text_node_to_html_node(x) for x in (text_to_textnodes(line[2:]))])
        root_node.children.append(child_node)
    return root_node
    
def ordered_list_to_html(block):
    root_node = ParentNode("ol", children=[])
    for line in block.split("\n"):
        line = line[line.find(". ")+2:]
        child_node = ParentNode("li", children=[text_node_to_html_node(x) for x in (text_to_textnodes(line))])
        root_node.children.append(child_node)
    return root_node
    
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    
    html_nodes = ParentNode("div", children=[])
    
    for block in blocks:
        block = block.strip()
        block_type = block_to_block_type(block)
        
        if block_type == block_type_paragraph:
            html_nodes.children.append(paragraph_block_to_html(block))
        elif block_type == block_type_code:
            html_nodes.children.append(code_block_to_html(block))
        elif block_type == block_type_heading:
            html_nodes.children.append(heading_block_to_html(block))
        elif block_type == block_type_quote:
            html_nodes.children.append(quote_block_to_html(block))
        elif block_type == block_type_unordered_list:
            html_nodes.children.append(unordered_list_to_html(block))
        elif block_type == block_type_ordered_list:
            html_nodes.children.append(ordered_list_to_html(block))
        else:
            raise ValueError("Invalid block type")
    return html_nodes