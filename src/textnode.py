from enum import Enum
import htmlnode

class TextType(Enum):
    TEXT = 'text'
    PLAIN = 'plain'
    BOLD = 'bold'
    ITALICS = 'italics'
    CODE = 'code'
    LINK = 'link'
    IMAGE = 'image'

class TextNode:
    def __init__(self, text_contents: str, text_type: TextType, this_url: str=None):
        self.text = text_contents
        self.type = text_type
        self.url = this_url
    
    def __eq__(self, other) -> bool:
        return self.text == other.text and self.type == other.type and self.url == other.url
    
    def __repr__(self) -> str:
        return f'TextNode({self.text}, {self.type.value}, {self.url})'
    
def text_node_to_html_node(text_node) -> htmlnode.LeafNode:
    match text_node.type:
        case TextType.TEXT:
            return htmlnode.LeafNode(tag=None, value=text_node.text)
        case TextType.BOLD:
            return htmlnode.LeafNode(tag='b', value=text_node.text)
        case TextType.ITALICS:
            return htmlnode.LeafNode(tag='i', value=text_node.text)
        case TextType.CODE:
            return htmlnode.LeafNode(tag='code', value=text_node.text)
        case TextType.LINK:
            return htmlnode.LeafNode(tag='a', value=text_node.text, props={'href': text_node.url})
        case TextType.IMAGE:
            return htmlnode.LeafNode(tag='img', value='', props={'src': text_node.url, 'alt': text_node.text})
    raise ValueError('Invalid TextNode specifications')
        
        


'''
It should handle each type of the TextType enum. If it gets a TextNode that is none of those types, it should raise an exception. 
Otherwise, it should return a new LeafNode object.

TextType.TEXT: This should return a LeafNode with no tag, just a raw text value.
TextType.BOLD: This should return a LeafNode with a "b" tag and the text
TextType.ITALIC: "i" tag, text
TextType.CODE: "code" tag, text
TextType.LINK: "a" tag, anchor text, and "href" prop
TextType.IMAGE: "img" tag, empty string value, "src" and "alt" props ("src" is the image URL, "alt" is the alt text)
'''