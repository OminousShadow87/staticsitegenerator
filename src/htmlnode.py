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
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value == None:
            raise ValueError
        if self.tag == None:
            return f"{self.value}"
        else:
            to_leaf = ""
            to_leaf += f"<{self.tag}"
            if self.props:
                to_leaf += f" {self.props_to_html()}"
            to_leaf += f">{self.value}</{self.tag}>"
            return to_leaf
        
    def __eq__(self, leafnode_2):
        return self.tag == leafnode_2.tag and self.value == leafnode_2.value and self.props == leafnode_2.props