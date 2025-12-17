from enum import Enum

class TextType(Enum):
    PLAIN = 'plain'
    BOLD = 'bold'
    ITALICS = 'italics'
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
    
