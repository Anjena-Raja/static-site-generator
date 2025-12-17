import unittest

from textnode import *


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
    
class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_text_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'b')
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_text_italics(self):
        node = TextNode("This is a text node", TextType.ITALICS)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'i')
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_text_code(self):
        node = TextNode("This is a text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'code')
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_text_link(self):
        node = TextNode("This is a text node", TextType.LINK, 'https://www.google.com')
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'a')
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props['href'], 'https://www.google.com')
    
    def test_text_image(self):
        node = TextNode("This is a text node", TextType.IMAGE, 'https://www.boot.dev/img/bootdev-logo-full-small.webp')
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'img')
        self.assertEqual(html_node.value, '')
        self.assertEqual(html_node.props['src'], 'https://www.boot.dev/img/bootdev-logo-full-small.webp')
        self.assertEqual(html_node.props['alt'], "This is a text node")

if __name__ == "__main__":
    unittest.main()