"""wikilinks.py
"""
import os
from .helper import get_all_files, readlines, dunderfy
import re
from collections import defaultdict
import sys
from pathlib import Path
from .wikilink import Wikilink

class MD_File:
    def __init__(self, name, path=None, exists=True):
        self.name = name
        self.path = path
        self.pattern = re.compile("(!)*\\[\\[(.+?)(?:\\]\\]|\\|(.+?)\\]\\])")
        self.content = [f'# {name}']
        if exists:
            self.content += readlines(path)
            for i, line in enumerate(self.content):
                if i == 0: continue # Don't indent the title
                if len(line) > 0 and line[0] == '#':
                    # Indent all headlines to make room 
                    # for the filename as main headline
                    self.content[i] = '#'+line
            self._make_wikilinks()
        self._exists = exists
        self.outgoing_links = []

    def _make_wikilinks(self):
        self.wikilinks = []
        for line in self.content:
            for match in self.pattern.finditer(line):
                wl = Wikilink(match.group(1), match.group(2), match.group(3))
                self.wikilinks.append(wl)
    
    def get_wikilinks(self):
        if self.exists:
            return self.wikilinks 
        return []

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
            self.content = [
                f'# {self.name}',
                'This Zettel was automatically created.']
        self.content.append("## Backlinks")
        if len(self.incoming_links) == 0:
            self.content.append('None')
        else:
            for link in self.incoming_links:
                self.content.append(f'- [[{link.name}]]')
    
    def get_content(self):
        return self.content

    @property
    def exists(self):
        return self._exists

class MD_Files:
    def __init__(self, dirs):
        self.dirs = dirs
        folder_path = dirs['notes']
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
                self.scr_paths[name] = Path(src_path)
                self.scr_paths[file] = Path(src_path)
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

    def get_content(self, name):
        if self.md_files[name].exists:
            return self.md_files[name].get_content()
class AssetsAndNotesLinks:
    def __init__(self, dirs):
        self.dirs = dirs
        self.assets = AssetLinks(dirs["assets"])
        self.notes = NoteLinks(dirs["notes"])
    def wikilink_to_link(self, wikilink):
        sw1 = self.assets.wikilink_exists(wikilink)
        sw2 = self.notes.wikilink_exists(wikilink)
        assert not (sw1 and sw2), "Ambiguous situation; should not exist."
        if sw1:
            # Die guten ins Kröpfchen, die schlechten ins Töpfchen.
            return self.assets.wikilink_to_link(wikilink)
        elif sw2:
            return self.notes.wikilink_to_link(wikilink)
        else:
            #return f'[[{wikilink}]]'
            return self.notes.wikilink_to_link(wikilink)
    def wikilink_to_path(self, wikilink):
        sw1 = self.assets.wikilink_exists(wikilink)
        sw2 = self.notes.wikilink_exists(wikilink)
        assert not (sw1 and sw2), "Ambiguous situation; should not exist."
        if sw1:
            # Die guten ins Kröpfchen, die schlechten ins Töpfchen.
            return self.assets.wikilink_to_path(wikilink)
        elif sw2:
            return self.notes.wikilink_to_path(wikilink)

class NoteLinks:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        files = get_all_files(folder_path)
        self.src_path = {}
        self.md_files = {}
        for file in files:
            name, ext = os.path.splitext(file)
            src_path = Path(f'{self.folder_path}/{file}')
            self.src_path[name] = src_path
            self.src_path[file] = src_path
            md_file = MD_File(name, src_path, True)
            self.md_files[name] = md_file
    def wikilink_exists(self, wikilink):
        return wikilink in self.src_path
    def wikilink_to_link(self, wikilink):
        if wikilink in self.md_files:
            return f'<a href="./{dunderfy(wikilink)}.xhtml"> {wikilink} </a>'
        return f'[[{wikilink}]]'
    def wikilink_to_path(self, wikilink):
        return self.src_path[wikilink]
    def get_content(self, name):
        md_file = self.md_files[name]
        return md_file.get_content()
class AssetLinks:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        files = get_all_files(folder_path)
        self.d = {}
        for file in files:
            self.d[file] = Path(f'{self.folder_path}/{file}')
    def wikilink_exists(self, wikilink):
        return wikilink in self.d
    def wikilink_to_link(self, wikilink):
        if wikilink in self.d:
            path = self.d[wikilink]
            if path.suffix in ['.png','.jpg','jpeg']:
                link = f'<img src="../assets/{dunderfy(wikilink)}" alt="{wikilink}"></img>'
                return link
            else:
                assert False, "Implement handling of extension " + path.suffix
        return f'[[{wikilink}]]'
    def wikilink_to_path(self, wikilink):
        return self.d[wikilink]
class Files:
    def __init__(self, dirs):
        self.dirs = dirs
        self.links = AssetsAndNotesLinks(dirs)
        self._make_outgoing_links()
        self._make_incoming_links()
    def get_content(self, name):
        res = self.links.notes.get_content(name)
        return res
    def _make_outgoing_links(self):
        new_md_files = []
        md_files = self.links.notes.md_files
        for name, md_file in md_files.items():
            wikilinks = md_file.get_wikilinks()
            current_md_files = []
            for wl in wikilinks:
                if wl.name in md_files:
                    md_file_tmp = md_files[wl.name]
                else:
                    md_file_tmp = MD_File(wl.name, exists=False)
                    new_md_files.append([wl.name, md_file_tmp])
                current_md_files.append(md_file_tmp)
            md_file.set_outgoing_links(current_md_files)
        for x, y in new_md_files:
            assert x not in md_files
            md_files[x] = y
    def _make_incoming_links(self):
        self.incoming_links = defaultdict(list)
        md_files = self.links.notes.md_files
        for md_filename, md_file in md_files.items():
            links = md_file.get_outgoing_links()
            for link in links:
                if md_filename not in self.incoming_links[link.name]:
                    self.incoming_links[link.name].append(md_file)
        # By going through all md_files, even those without incoming links,
        # we ensure that a file without backlinks ends on
        # "# Backlinks"
        # "- None"
        for name, md_file in md_files.items():
            inc_links = self.get_incoming_links(name)
            md_file.set_incoming_links(inc_links)

    def get_incoming_links(self, md_name):
        return self.incoming_links[md_name]

    def get_wikilinks(self, name):
        return self.links.notes.md_files[name].get_wikilinks()

# if __name__ == '__main__':
#     folder_path = 'Notes'
#     md_files = MD_Files(folder_path)