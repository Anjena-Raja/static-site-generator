from htmlnode import *
import unittest

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_multiple_props(self):
        props_dict = {
            "href": "https://www.google.com",
            "target": "_blank"
            }
        my_node = HTMLNode(tag='Mouse', value='house', props=props_dict)
        self.assertEqual(my_node.props_to_htlm(), ' href="https://www.google.com" target="_blank"')
    
    def test_props_to_html_one_prop(self):
        props_dict = {
            "href": "https://www.google.com"
            }
        my_node = HTMLNode(tag='Mouse', value='house', props=props_dict)
        self.assertEqual(my_node.props_to_htlm(), ' href="https://www.google.com"')
    
    def test_props_to_html_no_props(self):
        my_node = HTMLNode(tag='Mouse', value='house')
        self.assertEqual(my_node.props_to_htlm(), '')

        my_node = HTMLNode(tag='Mouse', value='house', props=dict())
        self.assertEqual(my_node.props_to_htlm(), '')

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_with_tag(self):
        node = LeafNode('p', 'Hello, world!')
        self.assertEqual(node.to_html(), '<p>Hello, world!</p>')
    
    def test_leaf_to_html_without_tag(self):
        node = LeafNode(None, 'Hello, world!')
        self.assertEqual(node.to_html(), 'Hello, world!')
    
    def test_leaf_to_html_with_property(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')
    
    def test_raises_value_error_when_no_value_provided(self):
        node = LeafNode('a', None)
        self.assertRaises(ValueError, node.to_html)

class TestParentNode(unittest.TestCase):
    def test_parent_to_html_with_multiple_children(self):
        node = ParentNode(
                    "p",
                    [
                        LeafNode("b", "Bold text"),
                        LeafNode(None, "Normal text"),
                        LeafNode("i", "italic text"),
                        LeafNode(None, "Normal text"),
                    ],
                )

        self.assertEqual(node.to_html(), '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>')

    def test_to_html_with_one_child(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_parent_to_html_without_tag(self):
        node = ParentNode(
                    None,
                    [
                        LeafNode("b", "Bold text"),
                        LeafNode(None, "Normal text"),
                        LeafNode("i", "italic text"),
                        LeafNode(None, "Normal text"),
                    ],
                )
        self.assertRaises(ValueError, node.to_html)

    def test_parent_to_html_without_children(self):
        node = ParentNode("p", None)
        self.assertRaises(ValueError, node.to_html)
    
    def test_parent_to_html_with_properties(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node], {"href": "https://www.google.com"})
        self.assertEqual(
            parent_node.to_html(),
            '<div href="https://www.google.com"><span><b>grandchild</b></span></div>',
        )


if __name__ == '__main__':
    unittest.main()