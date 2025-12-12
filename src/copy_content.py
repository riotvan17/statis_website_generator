import os
import shutil
from pathlib import Path
from blocks import markdown_to_html_node

TARGET_DIR = 'public'
SOURCE_DIR = 'static'
CONTENT_DIR = 'content'

def copy_content():
	for item in os.listdir(TARGET_DIR):
		item_path = os.path.join(TARGET_DIR, item)
		if os.path.isfile(item_path):
			os.unlink(item_path)
		elif os.path.isdir(item_path):
			shutil.rmtree(item_path)

	for item in os.listdir(SOURCE_DIR):
		s = os.path.join(SOURCE_DIR, item)
		t = os.path.join(TARGET_DIR, item)

		if os.path.isdir(s):
			shutil.copytree(s, t)
		else:
			shutil.copy(s, t)


def extract_title(markdown):
	for line in markdown.splitlines():
		if line.lstrip().startswith('# '):
			return line.lstrip('# ').strip()
		raise Exception


def generate_page(from_path, template_path, dest_path):
	print(f"Generating page from {from_path} to {dest_path} using {template_path}")
	with open(from_path) as f1:
		from_res = f1.read()
	with open(template_path) as f2:
		from_temp = f2.read()
	html = markdown_to_html_node(from_res).to_html()
	title = extract_title(from_res)
	from_temp = from_temp.replace("{{ Title }}", title)
	from_temp = from_temp.replace("{{ Content }}", html)
	from_temp = from_temp.replace('href="/', 'href="{from_path}')
	from_temp = from_temp.replace('src="/', 'src="{from_path}')
	dest_file = Path(dest_path)
	dest_file.parent.mkdir(parents=True, exist_ok=True)
	with open(dest_path, "w", ) as f3:
		f3.write(from_temp)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
	for item in os.listdir(dir_path_content):
		item_path = os.path.join(dir_path_content, item)
		dest_path = os.path.join(dest_dir_path, item)
		if os.path.isfile(item_path):
			dest_path = Path(dest_path).with_suffix(".html")
			generate_page(item_path, template_path, dest_path)
		elif os.path.isdir(item_path):
			generate_pages_recursive(item_path, template_path, dest_path)
	return