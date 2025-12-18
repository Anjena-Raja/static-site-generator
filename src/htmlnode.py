class HTMLNode:
    def __init__(self, tag: str|None=None, value: str|None=None, children: list|None=None, props: dict[str, str]|None=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_htlm(self):
        props_str = ''
        if self.props != None:
            for property, val in self.props.items():
                props_str += f' {property}="{val}"'

        return props_str

    def __repr__(self):
        return f'tag: {self.tag}, value: {self.value}, children: {self.children}, props: {self.props}'
    

class LeafNode(HTMLNode):
    def __init__(self, tag: str|None, value: str, props: dict[str, str]|None=None):
        super().__init__(tag=tag, value=value, props=props)
    
    def to_html(self) -> str:
        if self.value == None:
            raise ValueError
        
        if self.tag == None:
            return self.value
        
        return f'<{self.tag}{self.props_to_htlm()}>{self.value}</{self.tag}>'


class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list[HTMLNode], props: dict[str, str]|None=None):
        super().__init__(tag=tag, children=children, props=props)
    
    def to_html(self) -> str:
        if self.tag == None:
            raise ValueError('Tag must be present')
        
        if self.children == None:
            raise ValueError('No children provided')
        
        html_str = f'<{self.tag}{self.props_to_htlm()}>'
        for child in self.children:
            html_str += child.to_html()
        html_str += f'</{self.tag}>'
        
        return html_str       


'''
LeafNode("p", "This is a paragraph of text.").to_html()
"<p>This is a paragraph of text.</p>"
{
    "href": "https://www.google.com",
    "target": "_blank",
}
LeafNode("a", "Click me!", {"href": "https://www.google.com"}).to_html()
"<a href="https://www.google.com">Click me!</a>"
 href="https://www.google.com" target="_blank"
tag
Value
children
props
'''