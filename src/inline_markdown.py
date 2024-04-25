import re
from textnode import (
    TextNode,
    text_type_text,
    text_type_bold, 
    text_type_code,
    text_type_italic,
    text_type_image,
    text_type_link
)

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        if node.text.count(delimiter) % 2 != 0:
            raise ValueError("invalid markdown syntax")
        substr = node.text.split(delimiter)
        temp = []
        i = 0
        if node.text[:len(delimiter)] != delimiter:
            i += 1
        for text in substr:
            if text == "":
                continue
            if i % 2 == 0:
                temp.append(TextNode(text, text_type))
            else:
                temp.append(TextNode(text, text_type_text))
            i += 1
        new_nodes.extend(temp)
    return new_nodes

def extract_markdown_images(text):
    regexp = r"!\[(.*?)\]\((.*?)\)"
    matches = re.findall(regexp, text)
    return matches

def extract_markdown_links(text):
    regexp = r"[^!]\[(.*?)\]\((.*?)\)"
    matches = re.findall(regexp, text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        if node.text == "":
            continue
        matches = extract_markdown_images(node.text)
        if matches == []:
            new_nodes.append(node)
        else:
            temp = node.text
            for match in matches:
                substrs = temp.split(f"![{match[0]}]({match[1]})", 1)
                if substrs[0] != "":
                    new_nodes.append(TextNode(substrs[0], text_type_text))
                new_nodes.append(TextNode(match[0], text_type_image, match[1]))
                temp = substrs[1]
                
            if temp != "":
                new_nodes.append(TextNode(temp, text_type_text))
            
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        if node.text == "":
            continue
        matches = extract_markdown_links(node.text)
        if matches == []:
            new_nodes.append(node)
        else:
            temp = node.text
            for match in matches:
                substrs = temp.split(f"[{match[0]}]({match[1]})", 1)
                if substrs[0] != "":
                    new_nodes.append(TextNode(substrs[0], text_type_text))
                new_nodes.append(TextNode(match[0], text_type_link, match[1]))
                temp = substrs[1]
                
            if temp != "":
                new_nodes.append(TextNode(temp, text_type_text))
            
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, text_type_text)]
    
    # Split BOLD
    nodes = split_nodes_delimiter(nodes, "**", text_type_bold)
    # Split ITALICS
    nodes = split_nodes_delimiter(nodes, "*", text_type_italic)
    # Split CODE
    nodes = split_nodes_delimiter(nodes, "`", text_type_code)
    # Split IMAGES
    nodes = split_nodes_image(nodes)
    # Split LINKS
    nodes = split_nodes_link(nodes)
    
    return nodes