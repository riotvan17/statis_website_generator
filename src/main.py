import sys
from textnode import TextNode, TextType
from copy_content import copy_content, extract_title, generate_page, generate_pages_recursive

def old_1():
	new_node = TextNode("This is some anchor text", TextType('image'), "https://www.boot.dev")
	print(new_node)

def old_2():
	copy_content()

def old_3():
	copy_content()
	generate_page("content/index.md", "template.html", "public/index.html")

def old_4():
	copy_content("static", "public")
	generate_pages_recursive("content", "template.html", "public")

def main():
	basepath = "/"
	if len(sys.argv) > 1:
		basepath = sys.argv[1]
	copy_content("static", "docs")
	generate_pages_recursive("content", "template.html", "docs", basepath)

main()