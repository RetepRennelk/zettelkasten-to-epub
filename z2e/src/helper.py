import re
import os
import shutil
from jinja2 import Template, Environment, PackageLoader, select_autoescape
from datetime import datetime
import markdown
from .wikilink import Wikilink
from pathlib import Path

env = Environment(
    loader=PackageLoader(__name__),
    autoescape=select_autoescape())
md = markdown.Markdown()
zettel_template = env.get_template("zettel.xhtml")
epub_title = "PK's Zettelkasten"
OPF_identifier = "1234567890"
zettel_style_css = "./css/zettel_style.css"

writestr_cache = []
write_cache = []

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
    if target_path in writestr_cache:
        return
    else:
        with open(target_path, "w") as f:
            f.write(s)
        writestr_cache.append(target_path)

def write(source_path, target_path):
    if (source_path,target_path) in write_cache:
        return
    else:
        shutil.copy2(source_path, target_path)
        write_cache.append((source_path,target_path))

def prepare_folder_structure(epub_filename, dirs):
    temp_directory = dirs['temp']
    ops_dirname = dirs['ops']
    if os.path.exists(epub_filename):
        os.remove(epub_filename)
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

def write_content_opf(files, dirs):
    cache = []
    stack = [Wikilink(None, "ID0 Index", None)]
    nav_flag = True
    manifest_list = []
    spine_list = []
    while len(stack) > 0:
        head = stack.pop(0)
        if head in cache: continue
        src_path = files.links.wikilink_to_path(head.name)
        if src_path is None:
            src_path = Path(f'{head.name}.md')
        if src_path.suffix == ".md":
            target_filename, manifest_svg_links, manifest_link = \
                process_head(head.name, files, dirs)
            manifest_list.append(manifest_link)
            spine_list.append(head.name)
            manifest_list += manifest_svg_links
            wikilinks = get_wikilinks(files, head.name) 
            stack = wikilinks + stack
            cache.append(head)
            # gather_outgoing_links(head, wikilinks)
        if nav_flag:
            manifest_link = make_nav([head] + wikilinks, dirs)
            manifest_list.append(manifest_link)
            nav_flag = False
    manifest_link = write_zettel_style_css(dirs)
    manifest_list.append(manifest_link)
    manifest_list += store_assets(dirs)
    manifest = '\n    '.join(manifest_list)
    spine = '\n    '.join(make_spine(spine_list))
    date = datetime.today().strftime('%Y-%m-%dT%H:%M:%SZ')
    template = env.get_template("content.opf")
    f = f"./{dirs['temp']}/{dirs['ops']}/content.opf"
    s = template.render(date=date,manifest=manifest,spine=spine,OPF_identifier=OPF_identifier)
    writestr(s, f)

def process_head(head, files, dirs):
    head_stub = dunderfy(head)
    head_md = files.get_content(head)
    head_xhtml, manifest_svg_links = md_to_xhtml(head_md, head, head_stub, files, dirs)
    target_dir = f'{dirs["temp"]}/{dirs["ops"]}/xhtml'
    target_filename = store_xhtml(head_xhtml, head_stub, target_dir)
    manifest_link = xhtml_to_manifest(head_stub)
    return target_filename, manifest_svg_links, manifest_link

def md_to_xhtml(head_md, head, head_stub, files, dirs):
    """Syntax: md_to_xhtml(head_md)."""
    pattern = re.compile("(!)*\\[\\[(.+?)(?:\\]\\]|\\|(.+?)\\]\\])")
    xhtml_lst = []
    for line in head_md:
        idx = 0
        lst = []
        for match in pattern.finditer(line):
            span = match.span()
            lst.append(line[idx:span[0]])
            if is_image(match.group(2)):
                embed = match.group(1) == '!'
                link = handle_image(match.group(2), dirs, embed)
            else:
                if match.group(1) == "!": 
                    assert False, "Implement embedding"
                link = wikilink_to_link(files, match.group(2))
            lst.append(link)
            idx=span[1]
        lst.append(line[idx:])
        xhtml_lst.append(''.join(lst))
    # TODO xhtml_lst, manifest_png_links = math_to_png(xhtml_lst)
    manifest_png_links = []
    xhtml = md.convert('\n'.join(xhtml_lst))
    return zettel_template.render(
        title=head, head_stub=head_stub, body=xhtml,
        zettel_style_css="./css/zettel_style.css"), manifest_png_links

def wikilink_to_link(files, name):
    res = files.links.wikilink_to_link(name)
    return res

def store_xhtml(head_xhtml, head_stub, target_dir):
    target_filename = f"{target_dir}/{head_stub}.xhtml"
    writestr(head_xhtml, target_filename)
    return target_filename

def xhtml_to_manifest(head_stub):
    s = f'<item id="{head_stub}" href="xhtml/{head_stub}.xhtml" media-type="application/xhtml+xml"/>'
    return s

def get_wikilinks(files, head):
    """Syntax: get_wikilinks(head_md)."""
    wikilinks = files.get_wikilinks(head)
    return wikilinks

def make_spine(spine_list_in):
    spine_list_out = []
    for name in spine_list_in:
        name = dunderfy(name)
        spine_list_out.append(f'<itemref idref="{name}"/>')
    return spine_list_out

def make_nav(stack, dirs):
    items = [[f"./xhtml/{dunderfy(el.name)}.xhtml", el.name] for el in stack]
    template = env.get_template("nav.xhtml")
    s = template.render(epub_title=epub_title, items=items)
    writestr(s, f"./{dirs['temp']}/{dirs['ops']}/nav.xhtml")
    manifest_link = f'<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>'
    return manifest_link

def write_zettel_style_css(dirs):
    f = f"./{dirs['temp']}/{dirs['ops']}/xhtml/{zettel_style_css}"
    template = env.get_template("zettel_style.css")
    s = template.render()
    writestr(s, f)
    href = f"xhtml/{zettel_style_css}"
    manifest_link = f'<item id="css" href="{href}" media-type="text/css"/>'
    return manifest_link

def store_assets(dirs):
    manifest_links = []
    exts = {".png":"png",".jpeg":"jpeg",".jpg":"jpeg"}
    for root, _, files in os.walk(f'{dirs["assets"]}'):
        for file in files:
            source_path = Path(f'./{dirs["assets"]}/{file}')
            target_path = Path(f'./{dirs["temp"]}/{dirs["ops"]}/{dirs["assets"]}/{dunderfy(file)}')
            if source_path.suffix.lower() in ['.png','.jpg','jpeg']:
                write(source_path, target_path)
                id = dunderfy(file)
                href = f'./{dirs["assets"]}/{dunderfy(file)}'
                ext = exts[source_path.suffix.lower()]
                link = f'<item id="{id}" href="{href}" media-type="image/{ext}"/>'
                manifest_links.append(link)
    return manifest_links

def is_image(name):
    x = name.lower()
    return x.endswith('.jpg') or x.endswith('.jpeg') or x.endswith('.png')

def handle_image(name, dirs, embed):
    if embed == True:
        link = f'<img src="../{dirs["assets"]}/{name}">{name}</img>'
    else:
        template = env.get_template("image_container.xhtml")
        s = template.render(path=name)
        target_dir = f"{dirs['temp']}/{dirs['ops']}/{dirs['assets']}/{name}.xhtml"
        writestr(s, target_dir)
        target_dir = f"../{dirs['assets']}/{name}.xhtml"
        link = f'<a href="{target_dir}"> {name} </a>'
    return link