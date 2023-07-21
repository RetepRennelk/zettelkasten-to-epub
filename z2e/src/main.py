from z2e.src.helper import prepare_folder_structure,\
    write_container_xml, write_content_opf
from z2e.src.wikilinks import MD_Files, Files
import os
import shutil

def main():
    epub_filename = 'test.epub'
    dirs = dict(
        notes='Notes',
        assets='Assets',
        ops='OPS',
        temp='./.epub')
    prepare_folder_structure(epub_filename, dirs)
    write_container_xml(dirs)
    files = Files(dirs)
    write_content_opf(files, dirs)
    shutil.make_archive(epub_filename, root_dir=f'{dirs["temp"]}', format="zip")
    os.rename(epub_filename+'.zip', epub_filename)

if __name__ == '__main__':
    main()