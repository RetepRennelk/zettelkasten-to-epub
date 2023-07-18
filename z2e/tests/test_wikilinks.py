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

def test_md_files_outgoing_link():
    outlinks = md_files.get_outgoing_links("ID0 Index")
    outlinks = [x.name for x in outlinks]
    assert len(outlinks) == 2
    assert "ID1 Zettelkasten" in outlinks
    assert "ID2 Mathematics" in outlinks

    outlinks1 = md_files.get_outgoing_links("ID1 Zettelkasten")
    assert len(outlinks1)==0

    outlinks2 = md_files.get_outgoing_links("ID2 Mathematics")
    assert len(outlinks2)==0