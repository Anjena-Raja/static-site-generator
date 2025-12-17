import textnode
import htmlnode

def main():
    my_node = textnode.TextNode('This is some anchor text', textnode.TextType.LINK, 'https://www.boot.dev')
    print(my_node)
    my_node_2 = htmlnode.HTMLNode('mouse', 'house', 'louse', {'blouse': 'grouse', 'moose': 'shoes'})
    print(my_node_2.props_to_htlm())

if __name__ == '__main__':
    main()