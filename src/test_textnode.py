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

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_delimiter_present(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_nodes = [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ]
        for i in range(3):
            self.assertEqual(new_nodes[i], expected_nodes[i])
    
    def test_delimiter_present_multiple_times(self):
        node = TextNode("This `is text` with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_nodes = [
                TextNode("This ", TextType.TEXT),
                TextNode("is text", TextType.CODE),
                TextNode(" with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ]
        for i in range(5):
            self.assertEqual(new_nodes[i], expected_nodes[i])
    
    def test_delimiter_not_present(self):
        node = TextNode("This is text with a code block word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(node, new_nodes[0])
        self.assertEqual(len(new_nodes), 1)
    
    def test_delimeter_encompasses_entire_text(self):
        node = TextNode("`This is text with a code block word`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_nodes = [
                TextNode("", TextType.TEXT),
                TextNode("This is text with a code block word", TextType.CODE),
                TextNode("", TextType.TEXT),
            ]
        for i in range(3):
            self.assertEqual(new_nodes[i], expected_nodes[i])
    
    def test_unmatched_delimiter(self):
        node = TextNode("This is `text with a `code block` word", TextType.TEXT)
        self.assertRaises(ValueError, lambda: split_nodes_delimiter([node], '`', TextType.CODE))
    
    def test_multiple_nodes_with_matches(self):
        node1 = TextNode("This is text with a **code block** word", TextType.TEXT)
        node2 = TextNode("This **is also text with a code block** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node1, node2], '**', TextType.CODE)
        expected_nodes = [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
                TextNode("This ", TextType.TEXT),
                TextNode("is also text with a code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ]
        for i in range(6):
            self.assertEqual(new_nodes[i], expected_nodes[i])
    
    def test_multiple_nodes_without_matches(self):
        node1 = TextNode("This is text with a code block word", TextType.TEXT)
        node2 = TextNode("This is also text with a code block word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node1, node2], '`', TextType.CODE)
        self.assertEqual(new_nodes[0], node1)
        self.assertEqual(new_nodes[1], node2)

class TestFindingLinksAndImages(unittest.TestCase):
    def test_extract_single_image(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) that's really cool.")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_image_from_beginning(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)"
        self.assertEqual(extract_markdown_images(text), 
                         [("rick roll", "https://i.imgur.com/aKaOqIh.gif")])

    def test_extract_image_from_end(self):
        text = "This is text with ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(extract_markdown_images(text), 
                         [("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])

    def test_extract_multiple_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(extract_markdown_images(text), 
                         [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])
    
    def test_extract_single_link(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev)."
        matches = extract_markdown_links(text)
        self.assertEqual(matches, [("to boot dev", "https://www.boot.dev")])
    
    def test_extract_link_from_beginning(self):
        text = "[to boot dev](https://www.boot.dev) and "
        matches = extract_markdown_links(text)
        self.assertEqual(matches, [("to boot dev", "https://www.boot.dev")])

    def test_extract_link_from_end(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev)"
        matches = extract_markdown_links(text)
        self.assertEqual(matches, [("to boot dev", "https://www.boot.dev")])

    def test_extract_multiple_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        self.assertEqual(matches, [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])
    
    def test_extract_links_and_images_from_same_text(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and an image to ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        link_matches = extract_markdown_links(text)
        image_matches = extract_markdown_images(text)
        self.assertEqual(link_matches, [("to boot dev", "https://www.boot.dev")])
        self.assertEqual(image_matches, [("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])


if __name__ == "__main__":
    unittest.main()