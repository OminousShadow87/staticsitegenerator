import re
import os
import shutil
from enum import Enum
from htmlnode import *
from textnode import *

def text_node_to_html_node(text_node):
    match(text_node.text_type):
        case TextType.NORMAL_TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD_TEXT:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC_TEXT:
            return LeafNode("i", text_node.text)
        case TextType.CODE_TEXT:
            return LeafNode("code", text_node.text)
        case TextType.LINK_TEXT:
            return LeafNode("a", text_node.text, {"href":text_node.url})
        case TextType.IMAGE_TEXT:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception ("cannot match text type")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.NORMAL_TEXT:
            segments = node.text.split(delimiter)
            for index, segment in enumerate(segments):
                if index % 2 == 0:
                    new_nodes.append(TextNode(segment, TextType.NORMAL_TEXT))
                else:
                    new_nodes.append(TextNode(segment, text_type))
        else:
            new_nodes.append(node)
    return new_nodes

def extract_markdown_images(text):
    images = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return images

def extract_markdown_links(text):
    links = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return links

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        image_parts = extract_markdown_images(node.text)
        if not image_parts:
            new_nodes.append(node)
        for img_alt, img_url in image_parts:
            sections = node.text.split(f"![{img_alt}]({img_url})", 1)
            new_nodes.append(TextNode(sections[0], TextType.NORMAL_TEXT))
            new_nodes.append(TextNode(img_alt, TextType.IMAGE_TEXT, img_url))
            new_nodes.append(TextNode(sections[1], TextType.NORMAL_TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        link_parts = extract_markdown_links(node.text)
        if not link_parts:
            new_nodes.append(node)
        for link_text, link_url in link_parts:
            sections = node.text.split(f"[{link_text}]({link_url})", 1)
            new_nodes.append(TextNode(sections[0], TextType.NORMAL_TEXT))
            new_nodes.append(TextNode(link_text, TextType.LINK_TEXT, link_url))
            new_nodes.append(TextNode(sections[1], TextType.NORMAL_TEXT))
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.NORMAL_TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD_TEXT)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC_TEXT)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE_TEXT)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(markdown):
    block_str = []
    working_text = markdown.split("\n\n")
    for text in working_text:
        if text.strip():
            block_str.append(text.strip())
    return block_str

# function below identifies type of markdown
def block_to_block_type(block):
    if block.startswith("```") and block.endswith("```"): 
        return "code"
    elif (block.startswith("# ") or 
        block.startswith("## ") or 
        block.startswith("### ") or 
        block.startswith("#### ") or 
        block.startswith("##### ") or 
        block.startswith("###### ")):
        return "heading"
    lines = block.split("\n")
    if all(line.startswith(">") for line in lines):
        return "quote"
    elif all(line.startswith("* ") for line in lines) or all(line.startswith("- ") for line in lines):
        return "unordered_list"
    for i in range(1, len(lines) + 1):
        expected = f"{i}. "
        if not lines[i-1].startswith(expected):
            return "paragraph"
    return "ordered_list"

def extract_title(markdown):
    if not markdown.startswith("# "):
        raise Exception ("no header")
    return markdown[2:].strip()

def generate_page(from_path, template_path, dest_path):
    print (f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, 'r') as file:
        from_mkdown = file.read()
    with open(template_path, 'r') as file:
        template = file.read()
    html_node = markdown_to_html_node(from_mkdown)
    from_html = html_node.to_html()
    from_title = extract_title(from_mkdown)
    final_html = template.replace("{{ Title }}", f"{from_title}").replace("{{ Content }}", f"{from_html}")
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, 'w') as file:
        file.write(final_html)

def markdown_to_html_node(markdown):
    mkd_blocks = markdown_to_blocks(markdown)
    papa = ParentNode(tag = "div", children = [], props = {})
    for block in mkd_blocks:
        match(block_to_block_type(block)):
            case "code":
                code_leaf = LeafNode(tag = "code", value = block.strip('`').strip())
                code_parent = ParentNode(tag = "pre", children = [code_leaf])
                papa.children.append(code_parent)
            case "heading":
                hash_count = len(block) - len(block.lstrip('#'))
                heading_text = block[hash_count:].strip()
                heading_node = ParentNode(tag = f"h{hash_count}", children=text_to_children(heading_text))
                papa.children.append(heading_node)
            case "ordered_list":
                list_parent = ParentNode(tag = "ol", children = [])
                for line in block.splitlines():
                    list_text = line.split(maxsplit=1)[1].strip() 
                    list_leaf = ParentNode(tag = "li", children = text_to_children(list_text))
                    list_parent.children.append(list_leaf)  
                papa.children.append(list_parent)
            case "unordered_list":
                list_parent = ParentNode(tag = "ul", children = [])
                for line in block.splitlines():
                    list_text = line[1:].strip()
                    list_leaf = ParentNode(tag = "li", children = text_to_children(list_text))
                    list_parent.children.append(list_leaf)  
                papa.children.append(list_parent)               
            case "quote":
                quote_text = block.lstrip(">").strip()
                quote_node = ParentNode(tag = "blockquote", children = text_to_children(quote_text))
                papa.children.append(quote_node)
            case "paragraph":
                pg_text = block.strip()
                pg_node = ParentNode(tag="p", children=text_to_children(pg_text))
                papa.children.append(pg_node)
    return papa

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children