import unittest

from textnode import TextNode, TextType


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



if __name__ == "__main__":
    unittest.main()