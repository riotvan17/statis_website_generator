from textnode import BlockType
from htmlnode import ParentNode
from functions import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType
import re

def markdown_to_blocks(markdown):
	result = markdown.split("\n\n")
	stripped_list = [item.strip() for item in result]
	no_empty_list = [item for item in stripped_list if item != ""]
	final = [item.replace("\t\t", "") for item in no_empty_list]
	return final


def block_to_block_type(block):
	p_heading = r"^\#{1,6}\s\w+"
	p_code = r"^```\n.+\n```"
	p_quote = r"^>.+"
	p_unordered_list = r"^-\s.+"
	p_ordered_list = r"^\d+\.\s.+"

	match True:
		case _ if len(re.findall(p_heading, block)) > 0:
			return BlockType.HEADING
		case _ if len(re.findall(p_code, block)) > 0:
			return BlockType.CODE
		case _ if len(re.findall(p_quote, block)) > 0:
			return BlockType.QUOTE
		case _ if len(re.findall(p_unordered_list, block)) > 0:
			return BlockType.ULIST
		case _ if len(re.findall(p_ordered_list, block)) > 0:
			return BlockType.OLIST
		case _:
			return BlockType.PARAGRAPH


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.OLIST:
        return olist_to_html_node(block)
    if block_type == BlockType.ULIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    raise ValueError("invalid block type")


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)