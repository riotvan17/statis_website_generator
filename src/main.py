import sys
from textnode import TextNode, TextType
from copy_content import copy_content, extract_title, generate_page, generate_pages_recursive

basepath = sys.argv[0] if sys.argv[0] else "/"

def old_1():
	new_node = TextNode("This is some anchor text", TextType('image'), "https://www.boot.dev")
	print(new_node)

def old_2():
	copy_content()

def old_3():
	copy_content()
	generate_page("content/index.md", "template.html","public/index.html")

def old_4():
	copy_content()
	generate_pages_recursive("content", "template.html","public")

def main():
	generate_pages_recursive(basepath, "template.html", "public")

main()