from enum import Enum
import htmlnode
import re

class TextType(Enum):
    TEXT = 'text'
    PLAIN = 'plain'
    BOLD = 'bold'
    ITALICS = 'italics'
    CODE = 'code'
    LINK = 'link'
    IMAGE = 'image'

class TextNode:
    def __init__(self, text_contents: str, text_type: TextType, this_url: str|None=None):
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
        
def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, delimiter_type: TextType) -> list[TextNode]:
    new_text_nodes: list[TextNode] = list()
    for node in old_nodes:
        if node.type != TextType.TEXT:
            new_text_nodes.append(node)
        else:
            text_portions = node.text.split(delimiter)
            if len(text_portions) % 2 == 0:
                raise ValueError('Open delimeter is not closed')
            for i, text_portion in enumerate(text_portions):
                if i % 2 == 0:
                    new_text_nodes.append(TextNode(text_portion, TextType.TEXT))
                else:
                    new_text_nodes.append(TextNode(text_portion, delimiter_type))
    return new_text_nodes

def extract_markdown_images(markdown_text: str) -> list[tuple[str, str]]:
    matches = re.findall(r'\!\[(.+?)\]\((.+?)\)', markdown_text)
    return matches

def extract_markdown_links(markdown_text: str) -> list[tuple[str, str]]:
    matches = re.findall(r'(?<!!)\[(.+?)]\((.+?)\)', markdown_text)
    return matches


def split_nodes_for_link_or_image(old_nodes: list[TextNode], is_link: bool) -> list[TextNode]:
    new_text_nodes = list()
    for old_node in old_nodes:
        if is_link:
            matches = extract_markdown_links(old_node.text)
        else:
            matches = extract_markdown_images(old_node.text)

        unparsed_text = old_node.text
        for alt_text, url in matches:
            if is_link:
                non_link_text = unparsed_text[:unparsed_text.find(alt_text) - 1]
            else:
                non_link_text = unparsed_text[:unparsed_text.find(alt_text) - 2]

            unparsed_text = unparsed_text[unparsed_text.find(url) + len(url) + 1:]
            if len(non_link_text) > 0:
                new_text_nodes.append(TextNode(non_link_text, old_node.type))
            
            if is_link:
                new_text_nodes.append(TextNode(alt_text, TextType.LINK, url))
            else:
                new_text_nodes.append(TextNode(alt_text, TextType.IMAGE, url))

        if len(unparsed_text) > 0:
            new_text_nodes.append(TextNode(unparsed_text, old_node.type))
    return new_text_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    return split_nodes_for_link_or_image(old_nodes, True)
    

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    return split_nodes_for_link_or_image(old_nodes, False)
