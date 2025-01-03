import re
from enum import Enum
from htmlnode import *
from textnode import *
from funcs import *

def markdown_to_html_node(markdown):
    mkd_blocks = markdown_to_blocks(markdown)
    papa = ParentNode(tag = "div", children = [], props = {})
    for block in mkd_blocks:
        match(block_to_block_type(block)):
            case "code":
                code_leaf = LeafNode(tag = "code", value = block)
                code_parent = ParentNode(tag = "pre", children = [code_leaf])
                papa.children.append(code_parent)
            case "heading":
                hash_count = len(block) - len(block.lstrip('#'))
                heading_text = block[hash_count:].strip()
                heading_node = LeafNode(tag = f"h{hash_count}", value = heading_text)
                papa.children.append(heading_node)
            case "ordered_list":
                
            case "unordered_list":
                
            case "quote":
                quote_text = block.lstrip(">").strip()
                quote_node = LeafNode(tag = "blockquote", value = quote_text)
                papa.children.append(quote_node)
            case "paragraph":
                pg_text = block.strip()
                pg_node = LeafNode(tag = "p", value = pg_text)
                papa.children.append(pg_node)

    html_result = papa.to_html()
    return html_result