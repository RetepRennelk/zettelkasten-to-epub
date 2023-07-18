from z2e.src.wikilinks import MD_Files
from glob import glob

folder_path = './Notes'
md_files = MD_Files(folder_path)

def test_backlinks1():
    ref = """# ID0 Index

- [[ID1 Zettelkasten]]
- [[ID2 Mathematics]]
# Backlinks
None"""
    s = '\n'.join(md_files.md_files['ID0 Index'].content)
    assert ref==s

def test_backlinks2():
    ref = """# A Zettelkasten note
# Backlinks
- [[ID0 Index]]"""
    s = '\n'.join(md_files.md_files['ID1 Zettelkasten'].content)
    assert ref==s

def test_backlinks3():
    ref = """# ID2 Mathematics
# Backlinks
- [[ID0 Index]]"""
    s = '\n'.join(md_files.md_files['ID2 Mathematics'].content)
    assert ref==s