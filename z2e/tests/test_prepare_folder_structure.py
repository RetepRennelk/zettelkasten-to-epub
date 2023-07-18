
from z2e.src.helper import prepare_folder_structure
import os 

def test_prepare_folder_structure():
    epub_filename = 'test.epub'
    dir_names = dict(
        temp_directory='./.epub', 
        ops_dirname='OPS')
    prepare_folder_structure(epub_filename, dir_names)
    assert not os.path.exists(epub_filename)
    assert os.path.exists(f'{dir_names["temp_directory"]}/mimetype')
    assert os.path.exists(f'{dir_names["temp_directory"]}/{dir_names["ops_dirname"]}')
    assert os.path.exists(f'{dir_names["temp_directory"]}/META-INF')