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