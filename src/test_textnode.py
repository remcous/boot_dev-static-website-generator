import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        node3 = TextNode("This is a text node2", "bold")
        node4 = TextNode("This is a text node", "italic")
        node5 = TextNode("This is a text node", "bold", "https://www.boot.dev")
        self.assertEqual(node, node2)
        self.assertNotEqual(node, node3)
        self.assertNotEqual(node, node4)
        self.assertNotEqual(node, node5)
        
    def test_repr(self):
        node = TextNode("This is a text node", "bold")
        self.assertEqual(str(node), "TextNode(This is a text node, bold, None)")


if __name__ == "__main__":
    unittest.main()
