from enum import Enum

class TextType(Enum):
    NORMAL_TEXT = "normal"
    BOLD_TEXT = "bold"
    ITALIC_TEXT = "italics"
    CODE_TEXT = "code"
    LINK_TEXT = "links"
    IMAGE_TEXT = "images"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, textnode_2):
        return self.text == textnode_2.text and self.text_type == textnode_2.text_type and self.url == textnode_2.url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"