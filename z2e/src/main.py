from z2e.src.helper import prepare_folder_structure,\
    write_container_xml, write_content_opf
from z2e.src.wikilinks import MD_Files

def main():
    epub_filename = 'test.epub'
    dirs = dict(
        temp='./.epub', 
        ops='OPS',
        notes='Notes')
    prepare_folder_structure(epub_filename, dirs)
    write_container_xml(dirs)
    md_files = MD_Files(dirs['notes'])
    write_content_opf(md_files, dirs)