from z2e.src.helper import prepare_folder_structure

def main():
    epub_filename = 'test.epub'
    dir_names = dict(
        temp_directory='./.epub', 
        ops_dirname='OPS')
    prepare_folder_structure(epub_filename, dir_names)