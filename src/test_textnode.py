import unittest

from textnode import *
from funcs import *
from htmlnode import *

class Testmarkdown_to_html_node(unittest.TestCase):

    def test_heading_conversion(self):
        markdown = "### Heading Three"
        expected = ParentNode(
            "div",
            [LeafNode("h3", "Heading Three")],
            {}
        )
        self.assertEqual(markdown_to_html_node(markdown), expected)

    def test_unordered_list_conversion(self):
        markdown = "- First item\n- Second item"
        expected = ParentNode(
            "div",
            [
                ParentNode(
                    "ul",
                    [
                        LeafNode("li", "First item"),
                        LeafNode("li", "Second item")
                    ]
                )
            ],
            {}
        )   
        self.assertEqual(markdown_to_html_node(markdown), expected)

    def test_paragraph_with_inline_markdown(self):
        markdown = "This is *italic* and **bold** text"
        expected = ParentNode(
            "div",
            [
                ParentNode(
                    "p",
                    [
                        LeafNode("text", "This is "),
                        ParentNode("em", [LeafNode("text", "italic")]),
                        LeafNode("text", " and "),
                        ParentNode("strong", [LeafNode("text", "bold")]),
                        LeafNode("text", " text")
                    ]
                )
            ],
            {}
        )
        self.assertEqual(markdown_to_html_node(markdown), expected)

class TestMark2Blocks(unittest.TestCase):
    def testuno(self):
        input = "Battle of the Bands\nSex Bob-Ombs vs The Clash at Demonhead\n\nSex Bob-Ombs\nScott Pilgrim\nStephen Stills\nKim Pine\n\nThe Clash at Demonhead\nEnvy Adams\nTodd Ingram\nLynette Guycott"
        expected = [
            "Battle of the Bands\nSex Bob-Ombs vs The Clash at Demonhead",
            "Sex Bob-Ombs\nScott Pilgrim\nStephen Stills\nKim Pine",
            "The Clash at Demonhead\nEnvy Adams\nTodd Ingram\nLynette Guycott"
        ]
        result = markdown_to_blocks(input)
        self.assertEqual(result, expected)

    def testdos(self):
        input = "     Battle of the Bands\nSex Bob-Ombs vs The Clash at Demonhead     \n\n\n\n\n"
        expected = [
            "Battle of the Bands\nSex Bob-Ombs vs The Clash at Demonhead",
        ]
        result = markdown_to_blocks(input)
        self.assertEqual(result, expected)

    def testtres(self):
        input = "     Battle of the Bands\nSex Bob-Ombs vs The Clash at Demonhead     \n\nSex Bob-Ombs\nScott Pilgrim\nStephen Stills\nKim Pine\n\n\n\n\n\nThe Clash at Demonhead\nEnvy Adams\nTodd Ingram\nLynette Guycott"
        expected = [
            "Battle of the Bands\nSex Bob-Ombs vs The Clash at Demonhead",
            "Sex Bob-Ombs\nScott Pilgrim\nStephen Stills\nKim Pine",
            "The Clash at Demonhead\nEnvy Adams\nTodd Ingram\nLynette Guycott"
        ]
        result = markdown_to_blocks(input)
        self.assertEqual(result, expected)

    def testquad(self):
        input = "    "
        expected = []
        result = markdown_to_blocks(input)
        self.assertEqual(result, expected)


class TestTextNode1(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node, node2)

class TestTextNode2(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is some dooky", TextType.BOLD_TEXT)
        node2 = TextNode("This is some booty", TextType.BOLD_TEXT)
        self.assertNotEqual(node, node2)

class TestTextNode3(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.NORMAL_TEXT)
        self.assertNotEqual(node, node2)

class TestTextNode4(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is our fight song", TextType.IMAGE_TEXT, "https://old.reddit.com/")
        node2 = TextNode("This is our fight song", TextType.IMAGE_TEXT, "https://old.reddit.com/")
        self.assertEqual(node, node2)

class test_split_nodes_delimiter(unittest.TestCase):
    def test1(self):
        old_nodes = TextNode("This is text with a `code block` word", TextType.NORMAL_TEXT)
        delimiter = "`"
        text_type = TextType.CODE_TEXT
        expected = [
                        TextNode("This is text with a ", TextType.NORMAL_TEXT),
                        TextNode("code block", TextType.CODE_TEXT),
                        TextNode(" word", TextType.NORMAL_TEXT),
                    ]
        self.assertEqual(split_nodes_delimiter([old_nodes], delimiter, text_type), expected)

if __name__ == "__main__":
    unittest.main()