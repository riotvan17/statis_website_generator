import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
	def test_eq(self):
		node = HTMLNode()
		node2 = HTMLNode()
		self.assertEqual(print(node), print(node2))

	def test_props_to_html(self):
		props = {
				"href": "https://www.google.com",
				"target": "_blank",
			}
		output = ' href="https://www.google.com" target="_blank"'
		node = HTMLNode(props = props)
		self.assertEqual(node.props_to_html(), output)

	def test_diff_tag(self):
		node = HTMLNode()
		node2 = HTMLNode(tag="p")
		self.assertNotEqual(node, node2)

	def test_leaf_to_html_p(self):
		node = LeafNode("p", "Hello, world!")
		self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

	def test_to_html_with_children(self):
		child_node = LeafNode("span", "child")
		parent_node = ParentNode("div", [child_node])
		self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

	def test_to_html_with_grandchildren(self):
		grandchild_node = LeafNode("b", "grandchild")
		child_node = ParentNode("span", [grandchild_node])
		parent_node = ParentNode("div", [child_node])
		self.assertEqual(
			parent_node.to_html(),
			"<div><span><b>grandchild</b></span></div>",
    )


if __name__ == "__main__":
	unittest.main()