"""wikilinks.py
"""
import os
from .helper import get_all_files, readlines
import re
from collections import defaultdict
import sys

class Wikilink:
    def __init__(self, embed, name, alias):
        self.embed, self.name, self.alias = embed, name, alias

    def __str__(self):
        return f'embed={self.embed},name={self.name},alias={self.alias}'

class MD_File:
    def __init__(self, name, path=None, exists=True):
        self.name = name
        self.path = path
        self.pattern = re.compile("(!)*\\[\\[(.+?)(?:\\]\\]|\\|(.+?)\\]\\])")
        if exists:
            self.content = readlines(path)
            self._make_wikilinks()
        self.exists = exists
        self.outgoing_links = []

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

    def set_incoming_links(self, incoming_links):
        self.incoming_links = incoming_links
        self.add_backlinks()

    def get_incoming_links(self):
        return self.incoming_links

    def add_backlinks(self):
        if not self.exists:
            return
        self.content.append("# Backlinks")
        if len(self.incoming_links) == 0:
            self.content.append('None')
        else:
            for link in self.incoming_links:
                self.content.append(f'- [[{link.name}]]')

class MD_Files:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        files = get_all_files(folder_path)
        if len(files) == 0:
            print(f"No MD-files found in directory '{folder_path}'.")
            sys.exit(0)
        self.md_files = {}
        self.scr_paths = {}
        for file in files:
            src_path = f'{folder_path}/{file}'
            name, ext = os.path.splitext(file)
            if ext.lower() == '.md':
                self.md_files[name] = MD_File(name, src_path)
                self.scr_paths[name] = src_path
                self.scr_paths[file] = src_path
            else:
                print(f'Ignoring non-markdown file: {path}')
        self._make_outgoing_links()
        self._make_incoming_links()

    def _make_outgoing_links(self):
        new_md_files = []
        for name, md_file in self.md_files.items():
            wikilinks = md_file.get_wikilinks()
            md_files = []
            for wl in wikilinks:
                if wl.name in self.md_files:
                    md_file_tmp = self.md_files[wl.name]
                else:
                    md_file_tmp = MD_File(wl.name, exists=False)
                    new_md_files.append([wl.name, md_file_tmp])
                md_files.append(md_file_tmp)
            md_file.set_outgoing_links(md_files)
        for x, y in new_md_files:
            assert x not in self.md_files
            self.md_files[x] = y

    def _make_incoming_links(self):
        self.incoming_links = defaultdict(list)
        for md_filename, md_file in self.md_files.items():
            links = md_file.get_outgoing_links()
            for link in links:
                if md_filename not in self.incoming_links[link.name]:
                    print(link.name, md_file.name)
                    self.incoming_links[link.name].append(md_file)
        # By going through all md_files, even those without incoming links,
        # we ensure that a file without backlinks ends on
        # "# Backlinks"
        # "- None"
        for name, md_file in self.md_files.items():
            inc_links = self.get_incoming_links(name)
            md_file.set_incoming_links(inc_links)
    
    def get_outgoing_links(self, md_name):
        md_file = self.md_files[md_name]
        return md_file.get_outgoing_links()

    def get_incoming_links(self, md_name):
        return self.incoming_links[md_name]

    def get_source_path(self, identifier):
        if identifier in self.scr_paths:
            return self.scr_paths[identifier]

if __name__ == '__main__':
    folder_path = 'Notes'
    md_files = MD_Files(folder_path)