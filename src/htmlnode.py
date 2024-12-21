from enum import Enum

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
            # A string representing the HTML tag name (e.g. "p", "a", "h1", etc.)
        self.value = value
            # A string representing the value of the HTML tag (e.g. the text inside a paragraph)
        self.children = children
            # A list of HTMLNode objects representing the children of this node
        self.props = props
            # A dictionary of key-value pairs representing the attributes of the HTML tag

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        str_props = ""
        for x in self.props:
            str_props += f'{x}="{self.props[x]}" '
        return str_props.strip(" ")
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
    def __eq__(self, htmlnode_2):
        return self.tag == htmlnode_2.tag and self.value == htmlnode_2.value and self.children == htmlnode_2.children and self.props == htmlnode_2.props