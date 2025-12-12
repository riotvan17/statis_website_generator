import os
import shutil
from pathlib import Path
from blocks import markdown_to_html_node

def copy_content(source, target):
	for item in os.listdir(target):
		item_path = os.path.join(target, item)
		if os.path.isfile(item_path):
			os.unlink(item_path)
		elif os.path.isdir(item_path):
			shutil.rmtree(item_path)

	for item in os.listdir(source):
		s = os.path.join(source, item)
		t = os.path.join(target, item)

		if os.path.isdir(s):
			shutil.copytree(s, t)
		else:
			shutil.copy(s, t)


def extract_title(markdown):
	for line in markdown.splitlines():
		if line.lstrip().startswith('# '):
			return line.lstrip('# ').strip()
		raise Exception


def generate_page(from_path, template_path, dest_path, basepath):
	print(f"Generating page from {from_path} to {dest_path} using {template_path}")
	with open(from_path) as f1:
		from_res = f1.read()
	with open(template_path) as f2:
		from_temp = f2.read()
	html = markdown_to_html_node(from_res).to_html()
	title = extract_title(from_res)
	from_temp = from_temp.replace("{{ Title }}", title)
	from_temp = from_temp.replace("{{ Content }}", html)
	from_temp = from_temp.replace('href="/', f'href="{basepath}')
	from_temp = from_temp.replace('src="/', f'src="{basepath}')
	dest_file = Path(dest_path)
	dest_file.parent.mkdir(parents=True, exist_ok=True)
	with open(dest_path, "w", ) as f3:
		f3.write(from_temp)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
	for item in os.listdir(dir_path_content):
		item_path = os.path.join(dir_path_content, item)
		dest_path = os.path.join(dest_dir_path, item)
		if os.path.isfile(item_path):
			dest_path = Path(dest_path).with_suffix(".html")
			generate_page(item_path, template_path, dest_path, basepath)
		elif os.path.isdir(item_path):
			generate_pages_recursive(item_path, template_path, dest_path, basepath)
	return