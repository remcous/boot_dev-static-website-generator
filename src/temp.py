from markdown_blocks import markdown_to_html_node

md = """
> This is a
> blockquote block

this is paragraph text

"""

node = markdown_to_html_node(md)
html = node.to_html()

print(html)
print("<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>")