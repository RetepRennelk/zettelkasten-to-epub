from glob import glob
import os
from collections import defaultdict
from pathlib import Path
from helper import dunderfy, get_all_files
from wikilinks import MD_File



class Links:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.files = self.get_all_files()
        self.name_and_ext = self.get_name_and_ext()
        
    def get_name_and_ext(self):
        name_and_ext = defaultdict(list)
        for file in self.files:
            name, ext = os.path.splitext(file)
            name_and_ext[Path(name)].append(ext.lower())
        return name_and_ext

    def get_all_files(self):
        file_list = []
        for root, dirs, files in os.walk(self.folder_path):
            #for file in files:
            #    file_list.append(os.path.join(root, file))
            file_list += files
        return file_list

    def wikilink_to_link(self, wikilink):
        name, ext = os.path.splitext(wikilink)
        path = Path(name)
        if ext == '' or ext=='.md':
            if path in self.name_and_ext and '.md' in self.name_and_ext[path]:
                return f'<a href="./{name.replace(" ","_")}.xhtml"> {name} </a>'
            return f'[[{wikilink}]]'
        assert False, f'Implement handling of file with extension: {ext}'
        if ext in ['.png', '.jpeg', '.jpg']:
            if path in self.name_and_ext and ext in self.name_and_ext[path]:
                return f'<img src="assets/{wikilink.replace(" ","_")}" alt="{wikilink}">'
        if ext == '.pdf':
             return f'<a href="assets/{wikilink}"> {wikilink}</a>'

    def wikilink_to_path(self, wikilink):
        name, ext = os.path.splitext(wikilink)
        path = Path(name)
        if ext == '' or ext=='.md':
            if path in self.name_and_ext and '.md' in self.name_and_ext[path]:
                return Path(f'{self.folder_path}/{name}.md')
        if ext in ['.png', '.jpeg', '.jpg']:
            if path in self.name_and_ext and ext in self.name_and_ext[path]:
                return 
        if ext == '.pdf':
             return 
    
    def get_path_from_wikilink(self, wikilink):
        name, ext = os.path.splitext(wikilink)
        ext = ext.lower()
        path = Path(name)
        if ext == '' or ext=='.md':
            if path in self.name_and_ext and '.md' in self.name_and_ext[path]:
                return Path(self.folder_path) / path + '.md'
        elif ext in ['.png', '.jpeg', '.jpg', '.pdf']:
            if path in self.name_and_ext and ext in self.name_and_ext[path]:
                return Path(self.folder_path) / path + ext

if __name__ == '__main__':
    links = Links('./notes')
    wikilink = "ID00 Index.md"
    print(links.wikilink_to_path(wikilink))
    