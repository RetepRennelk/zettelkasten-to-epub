"""wikilinks.py
"""
import os
from .helper import get_all_files, readlines
import re
from collections import defaultdict

class Wikilink:
    def __init__(self, embed, name, alias):
        self.embed, self.name, self.alias = embed, name, alias

    def __str__(self):
        return f'embed={self.embed},name={self.name},alias={self.alias}'

class MD_File:
    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.pattern = re.compile("(!)*\\[\\[(.+?)(?:\\]\\]|\\|(.+?)\\]\\])")
        self.content = readlines(path)
        self._make_wikilinks()

    def _make_wikilinks(self):
        self.wikilinks = []
        for line in self.content:
            for match in self.pattern.finditer(line):
                wl = Wikilink(match.group(1), match.group(2), match.group(3))
                self.wikilinks.append(wl)
    
    def get_wikilinks(self):
        return self.wikilinks

    def set_outgoing_links(self, outgoing_links):
        self.outgoing_links = outgoing_links

    def get_outgoing_links(self):
        return self.outgoing_links

class MD_Files:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        files = get_all_files(folder_path)
        self.md_files = {}
        for file in files:
            path = f'{folder_path}/{file}'
            name, ext = os.path.splitext(file)
            if ext.lower() == '.md':
                self.md_files[name] = MD_File(name, path)
            else:
                print(f'Ignoring non-markdown file: {path}')
        self._make_outgoing_links()
        self._make_incoming_links()

    def _make_outgoing_links(self):
        for name, md_file in self.md_files.items():
            wikilinks = md_file.get_wikilinks()
            md_files = [self.md_files[wl.name] for wl in wikilinks]
            md_file.set_outgoing_links(md_files)

    def _make_incoming_links(self):
        self.incoming_links = defaultdict(list)
        for md_filename, md_file in self.md_files.items():
            for link in md_file.get_outgoing_links():
                print("Link: ", link.name)
                if md_filename not in self.incoming_links[link.name]:
                    self.incoming_links[link.name].append(md_file)
    
    def get_outgoing_links(self, md_name):
        md_file = self.md_files[md_name]
        return md_file.get_outgoing_links()

    def get_incoming_links(self, md_name):
        return self.incoming_links[md_name]

if __name__ == '__main__':
    folder_path = 'Notes'
    md_files = MD_Files(folder_path)