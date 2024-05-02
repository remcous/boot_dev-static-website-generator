import re
import markdown_blocks
import os
import pathlib

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for filename in os.listdir(dir_path_content):
        if os.path.isfile(filename) and os.path.splitext(filename)[1] != ".md":
            continue
        
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)

        if os.path.isfile(from_path):
            dest_path = os.path.splitext(dest_path)[0] + ".html"
            generate_page(from_path, dest_path, template_path)
        else:
            generate_pages_recursive(from_path, template_path, dest_path)

def generate_page(from_path, dest_path, template_path):
    # Print a message to the console that says something like "Generating page from from_path to dest_path using template_path".
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    # Read the markdown file at from_path and store the contents in a variable.
    with open(from_path) as file:
        markdown = file.read()
    
    # Read the template file at template_path and store the contents in a variable.
    with open(template_path) as file:
        template = file.read()
    
    # Use your markdown_to_html_node function and .to_html() method to convert the markdown file to HTML.
    html = markdown_blocks.markdown_to_html_node(markdown).to_html()
    
    # Use the extract_title function to grab the title of the page.
    title = extract_title(markdown)
    
    # Replace the {{ Title }} and {{ Content }} placeholders in the template with the HTML and title you generated.
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    
    # Write the new HTML to a file at dest_path. Be sure to create any necessary directories if they don't exist.
    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))
        
    with open(dest_path, "w") as file:
        file.write(template)
    
    print("Complete")

def extract_title(markdown):
    exp = "#{1} (.+)\n"
    match = re.search(exp, markdown)
    if match is None:
        raise ValueError
    return match[1]