import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq_without_url(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_with_url(self):
        node = TextNode("This is a text node", TextType.LINK, 'https://www.boot.dev/dashboard')
        node2 = TextNode("This is a text node", TextType.LINK, 'https://www.boot.dev/dashboard')
        self.assertEqual(node, node2)
    
    def test_eq_different_links(self):
        node = TextNode("This is a text node", TextType.LINK, 'https://www.boot.dev')
        node2 = TextNode("This is a text node", TextType.LINK, 'https://www.boot.dev/dashboard')
        self.assertNotEqual(node, node2)
    
    def test_eq_different_types(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALICS)
        self.assertNotEqual(node, node2)
    
    def test_eq_different_text(self):
        node = TextNode("This is a text", TextType.PLAIN)
        node2 = TextNode("This is also text", TextType.PLAIN)
        self.assertNotEqual(node, node2)
    
    def test_repr_no_url(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node.__repr__(), 'TextNode(This is a text node, bold, None)')
    
    def test_repr_with_url(self):
        node = TextNode("This is a text node", TextType.LINK, 'https://www.boot.dev')
        self.assertEqual(node.__repr__(), 'TextNode(This is a text node, link, https://www.boot.dev)')
    


if __name__ == "__main__":
    unittest.main()