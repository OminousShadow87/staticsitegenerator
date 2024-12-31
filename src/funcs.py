import re
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