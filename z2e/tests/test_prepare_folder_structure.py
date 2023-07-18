
from z2e.src.helper import prepare_folder_structure
import os 

def test_prepare_folder_structure():
    epub_filename = 'test.epub'
    dirs = dict(
        temp='./.epub', 
        ops='OPS')
    prepare_folder_structure(epub_filename, dirs)
    assert not os.path.exists(epub_filename)
    assert os.path.exists(f'{dirs["temp"]}/mimetype')
    assert os.path.exists(f'{dirs["temp"]}/{dirs["ops"]}')
    assert os.path.exists(f'{dirs["temp"]}/META-INF')