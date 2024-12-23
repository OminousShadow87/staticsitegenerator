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

class LeafTextNode1(unittest.TestCase):
    def test_leaf(self):
        node = LeafNode(
            tag="a",
            value="Click me!",
            props={"href": "https://www.google.com"}
                        )
        expected = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(node.to_html(), expected)

class LeafTextNode2(unittest.TestCase):
    def test_leaf(self):
        node = LeafNode(
            tag="b",
            value="Santa Baby",
                        )
        expected = '<b>Santa Baby</b>'
        self.assertEqual(node.to_html(), expected)

class ParentNode1(unittest.TestCase):
    def test_parent(self):
        node = ParentNode("div", [
            ParentNode("section", [
                ParentNode("article", [
                    LeafNode("h1", "Inception"),
                    ParentNode("p", [
                        LeafNode("b", "We need to go"),
                        LeafNode(None, " "),
                        LeafNode("i", "deeper"),
                    ])
                ])
            ])
        ])
        expected = '<div><section><article><h1>Inception</h1><p><b>We need to go</b> <i>deeper</i></p></article></section></div>'
        self.assertEqual(node.to_html(), expected)

class ParentNode2(unittest.TestCase):
    def test_parent(self):
        node = ParentNode("", [
            ParentNode("section", [
                ParentNode("article", [
                    LeafNode("h1", "Inception"),
                    ParentNode("p", [
                        LeafNode("b", "We need to go"),
                        LeafNode(None, " "),
                        LeafNode("i", "deeper"),
                    ])
                ])
            ])
        ])
        self.assertRaisesRegex(ValueError, "No tag")

class ParentNode3(unittest.TestCase):
    def test_parent(self):
        node = ParentNode("div", None, None)
        with self.assertRaisesRegex(ValueError, "No children"):
            node.to_html()


class ParentNode4(unittest.TestCase):
    def test_parent(self):
        node = ParentNode("div", None, None)
        with self.assertRaisesRegex(ValueError, "No children"):
            node.to_html()

    def test_parent_no_tag(self):
        node = ParentNode(None, ["some child"], None)
        with self.assertRaisesRegex(ValueError, "No tag"):
            node.to_html()

    def test_parent_valid(self):
        node = ParentNode("div", [LeafNode("p", "hello")], None)
        self.assertEqual(node.to_html(), "<div><p>hello</p></div>")

if __name__ == "__main__":
    unittest.main()