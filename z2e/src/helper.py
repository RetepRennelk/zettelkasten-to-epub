import re
import os
import shutil
from jinja2 import Template, Environment, PackageLoader, select_autoescape

env = Environment(
    loader=PackageLoader(__name__),
    autoescape=select_autoescape())

def dunderfy(s):
    return s.replace("_", "__").replace(" ","_")

def get_all_files(folder_path):
    file_list = []
    for root, dirs, files in os.walk(folder_path):
        #for file in files:
        #    file_list.append(os.path.join(root, file))
        file_list += files
    return file_list

def readlines(filename):
    with open(filename) as f:
        file_content = f.read().rstrip("\n")
    return file_content.split("\n")

def writestr(s, target_path):
    with open(target_path, "w") as f:
        f.write(s)

def write(source_path, target_path):
    shutil.copy2(source_path, target_path)

def prepare_folder_structure(epub_filename, dirs):
    temp_directory = dirs['temp']
    ops_dirname = dirs['ops']
    if os.path.exists(epub_filename):
        os.remove(self.epub_filename)
    if os.path.exists(temp_directory):
        shutil.rmtree(temp_directory)
    directories = [
        f'{temp_directory}/META-INF', 
        f'{temp_directory}/{ops_dirname}',
        f'{temp_directory}/{ops_dirname}/assets',
        f'{temp_directory}/{ops_dirname}/xhtml',
        f'{temp_directory}/{ops_dirname}/xhtml/css']
    for directory in directories:
        os.makedirs(directory)
    writestr("application/epub+zip", f'{temp_directory}/mimetype')

def write_container_xml(dirs):
    template = env.get_template("container.xml")
    s = template.render(ops_dir=dirs['ops'])
    writestr(s, f'{dirs["temp"]}/META-INF/container.xml')

def write_content_opf(md_files, dirs):
    cache = {}
    stack = ["ID0 Index"]
    while len(stack) > 0:
        head = stack.pop(0)
        if head in cache: continue
