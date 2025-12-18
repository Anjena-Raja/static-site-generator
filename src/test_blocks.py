import unittest

from blocks import *

class TestMarkdownToBlocks(unittest.TestCase):
    def test_single_block(self):
        md = """
- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "- This is a list\n- with items",
            ],
        )

    def test_multiple_blocks_single_empty_space(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_multiple_blocks_with_extra_spaces(self):
        md = """
This is **bolded** paragraph



This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line





- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_extra_spaces_and_tabs_surrounding_blocks(self):
        md = """
         This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

        - This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        block0 = ' Header??? '
        block1 = '# Heading 1'
        block2 = '##  Heading 2'
        block3 = '### Heading' \
        '3'
        block4 = '#### Heading 4'
        block5 = '#####          ' \
        '' \
        '' \
        '5'
        block6 = '###### Heading6   '
        block7 = '####### Unfortunately not a header, 7'
        block4_but_no_space = '####4:('
        for block in [block1, block2, block3, block4, block5, block6]:
            self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        for block in [block0, block4_but_no_space, block7]:
            self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_code(self):
        code1 = '```print("Hello, World!")```'
        code2 = '```print("Jello World!")\n```'
        code3 = '```             ```'
        code4 = '``````'
        for block in [code1, code2, code3, code4]:
            self.assertEqual(block_to_block_type(block), BlockType.CODE)
    
    def test_quote(self):
        quote1 = '''> My name is mouse. \n> I live in 123 house. \n> Bye!'''
        quote2 = '> Do you like cheese?'
        quote3 = '>I am also a quote'
        
        self.assertEqual(block_to_block_type(quote1), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(quote2), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(quote3), BlockType.QUOTE)
    
    def test_unordered_list(self):
        list1 = '- This list has only one element'
        list2 = '- This has multiple\n- It has this 2nd element\n- And a third one too!'
        missing_space_after_dash = '-I would have been a list had I a space :('
        not_all_dashes = '- This looks like its a lis\nBut this line lacks a dash\n- So it is not'

        self.assertEqual(block_to_block_type(list1), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type(list2), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type(missing_space_after_dash), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(not_all_dashes), BlockType.PARAGRAPH)
    
    def test_ordered_list(self):
        list1 = '1. Milk\n2. Cheese \n3. Please?'
        list2 = '1. Snail'
        not_starting_with_one = '2. Cookie \n3. I forgot #1'
        non_sequential_numbers = '1. Tomato Juice\n3. Oh dearie me.'
        not_all_nums = 'Here is the title of my list\n1. And now it is not a list'

        self.assertEqual(block_to_block_type(list1), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type(list2), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type(not_starting_with_one), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(non_sequential_numbers), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(not_all_nums), BlockType.PARAGRAPH)



if __name__ == "__main__":
    unittest.main()