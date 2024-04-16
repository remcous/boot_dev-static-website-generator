import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_to_html(self):
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()
            
    def test_props_to_html(self):
        node = HTMLNode("a", "Boot.dev", None, {"href": "https://www.boot.dev"})
        self.assertEqual(node.props_to_html(), " href=\"https://www.boot.dev\"")
    
    def test_repr(self):
        node = HTMLNode("a", "Boot.dev", None, {"href": "https://www.boot.dev"})
        self.assertEqual(str(node), f"HTMLNode(a, Boot.dev, None, {{'href': 'https://www.boot.dev'}})")
        
class TestLeafNode(unittest.TestCase):
    def test_to_html1(self):
        node = LeafNode()
        with self.assertRaises(ValueError):
            node.to_html()
            
    def test_to_html2(self):
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(node.to_html(), "<p>This is a paragraph of text.</p>")
        
    def test_to_html3(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "<a href=\"https://www.google.com\">Click me!</a>")
        
class TestParentNode(unittest.TestCase):
    def test_to_html1(self):
        # No tag provided
        node = ParentNode(children=[LeafNode("p", "This is a paragraph of text.")], props={})
        with self.assertRaises(ValueError):
            node.to_html()
            
    def test_to_html2(self):
        # No children provided
        node = ParentNode(tag="h1", props={})
        with self.assertRaises(ValueError):
            node.to_html()
            
    def test_to_html3(self):
        # Parent with one child LeafNode
        node = ParentNode(tag="b", children=[
            LeafNode("p", "This is a paragraph of text.")
        ], props={})
        self.assertEqual(node.to_html(), f"<b><p>This is a paragraph of text.</p></b>")
        
    def test_to_html4(self):
        # Parent with a nested Parent
        node = ParentNode(tag="p", children=[
            ParentNode(tag="h1", children=[
                LeafNode(tag="b", value="Hello world")
            ])
        ])
        self.assertEqual(node.to_html(), "<p><h1><b>Hello world</b></h1></p>")
        
    def test_to_html5(self):
        # Parent with 2 leaves
        node = ParentNode(tag="p", children=[
            LeafNode('i', value="italic text"),
            LeafNode("a", "hyperlink", props={"href": "www.google.com"})
        ])
        
        self.assertEqual(node.to_html(), "<p><i>italic text</i><a href=\"www.google.com\">hyperlink</a></p>")
        
if __name__ == "__main__":
    unittest.main()