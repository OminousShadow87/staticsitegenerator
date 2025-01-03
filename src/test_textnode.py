import unittest

from textnode import *
from funcs import *
from mark2html import *
class Testmarkdown_to_html_node(unittest.TestCase):

    def test_code_block_conversion(self):
        markdown = "```\ncode snippet\n```"
        expected = "<div><pre><code>code snippet</code></pre></div>"
        self.assertEqual(markdown_to_html_node(markdown), expected)

    def test_heading_conversion(self):
        markdown = "### Heading Three"
        expected = "<div><h3>Heading Three</h3></div>"
        self.assertEqual(markdown_to_html_node(markdown), expected)

    def test_ordered_list_conversion(self):
        markdown = "1. First item\n2. Second item"
        expected = "<div><ol><li>First item</li><li>Second item</li></ol></div>"
        self.assertEqual(markdown_to_html_node(markdown), expected)

    def test_unordered_list_conversion(self):
        markdown = "- First item\n- Second item"
        expected = "<div><ul><li>First item</li><li>Second item</li></ul></div>"
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