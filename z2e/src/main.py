from z2e.src.helper import prepare_folder_structure,\
    write_container_xml

def main():
    epub_filename = 'test.epub'
    dirs = dict(
        temp='./.epub', 
        ops='OPS')
    prepare_folder_structure(epub_filename, dirs)
    write_container_xml(dirs)