from z2e.src.wikilinks import MD_Files
from glob import glob

folder_path = './Notes'
md_files = MD_Files(folder_path)

def test_md_files():
    N_files = len(glob(f'{folder_path}/*.md'))
    assert N_files == len(md_files.md_files)
    assert 'ID0 Index' in md_files.md_files
    assert 'ID1 Zettelkasten' in md_files.md_files
    assert 'ID2 Mathematics' in md_files.md_files