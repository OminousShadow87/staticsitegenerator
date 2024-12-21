import unittest

from htmlnode import *


class HTMLTextNode1(unittest.TestCase):
    def test_to_html(self):
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()

class HTMLTextNode2(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        expected = 'href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected)

class HTMLTextNode3(unittest.TestCase):
    def test_full_initialization(self):
        node = HTMLNode(
            tag="a",
            value="Link",
            children=[HTMLNode(tag="b", value="bold")],
            props={"href": "https://www.example.com"}
        )
        
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, "Link")
        self.assertEqual(node.children, [HTMLNode(tag="b", value="bold")])
        self.assertEqual(node.props, {"href": "https://www.example.com"})



if __name__ == "__main__":
    unittest.main()