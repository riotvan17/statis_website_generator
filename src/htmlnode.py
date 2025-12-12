class HTMLNode():
	def __init__(self, tag=None, value=None, children=None, props=None):
		self.tag = tag
		self.value = value
		self.children = children
		self.props = props

	def to_html(self):
		raise NotImplementedError

	def props_to_html(self):
		output = ""
		if self.props is not None:
			for i in self.props:
				output += f' {i}="{self.props[i]}"'
		return output

	def __repr__(self):
		return(f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})")


class LeafNode(HTMLNode):
	def __init__(self, tag, value, props=None):
		super().__init__(tag, value, None, props)

	def to_html(self):
		if self.value is None:
			return ValueError
		if self.tag is None:
			return self.value
		html_tag = f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
		return html_tag

	def __repr__(self):
		return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
	def __init__(self, tag, children, props=None):
		super().__init__(tag, None, children, props)

	def to_html(self):
		if self.tag is None:
			return ValueError("no tag")
		if self.children is None:
			return ValueError("no children")
		html_tag = f"<{self.tag}{self.props_to_html()}>"
		for l in self.children:
			html_tag += l.to_html()
		html_tag += f"</{self.tag}>"
		return html_tag

	def __repr__(self):
		return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
