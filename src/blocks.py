from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = 'paragraph'
    HEADING = 'heading'
    CODE = 'code'
    QUOTE = 'quote'
    UNORDERED_LIST = 'unordered_list'
    ORDERED_LIST = 'ordered_list'

def markdown_to_blocks(markdown: str) -> list[str]:
    split_blocks: list[str] = markdown.split('\n\n')
    blocks_without_extra_whitespace: list[str] = []
    for block in split_blocks:
        stripped_block = block.strip()
        if len(stripped_block) > 0:
            blocks_without_extra_whitespace.append(stripped_block)
    return blocks_without_extra_whitespace

def block_to_block_type(block: str) -> BlockType:
    if re.search(r'^(#{1,6}) ', block) != None:
        return BlockType.HEADING
    elif re.search(r'^```[\s\S]*```$', block) != None:
        return BlockType.CODE
    elif all(line.startswith('>') for line in block.split('\n')):
        return BlockType.QUOTE
    elif all(line.startswith('- ') for line in block.split('\n')):
        return BlockType.UNORDERED_LIST
    elif all(line.startswith(f'{i + 1}. ') for i, line in enumerate(block.split('\n'))):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH


'''
Create a block_to_block_type function that takes a single block of markdown text as input and returns the BlockType representing the type of block it is. You can assume all leading and trailing whitespace were already stripped (we did that in a previous lesson).
Headings start with 1-6 # characters, followed by a space and then the heading text.
Code blocks must start with 3 backticks and end with 3 backticks.
Every line in a quote block must start with a > character.
Every line in an unordered list block must start with a - character, followed by a space.
Every line in an ordered list block must start with a number followed by a . character and a space. The number must start at 1 and increment by 1 for each line.
If none of the above conditions are met, the block is a normal paragraph.
'''