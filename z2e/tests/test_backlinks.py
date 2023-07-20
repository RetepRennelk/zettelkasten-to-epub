from z2e.src.wikilinks import MD_Files
from glob import glob

dirs = dict(notes='./Notes')
md_files = MD_Files(dirs)

def test_backlinks1():
    ref = """# ID0 Index

- [[ID1 Zettelkasten]]
- [[ID2 Mathematics]]
- [[ID3 A note that doesn't exist]]
# Backlinks
None"""
    s = '\n'.join(md_files.md_files['ID0 Index'].content)
    print(s)
    assert ref==s

def test_backlinks2():
    ref = """# A Zettelkasten note
# Backlinks
- [[ID0 Index]]"""
    s = '\n'.join(md_files.md_files['ID1 Zettelkasten'].content)
    print(s)
    assert ref==s

def test_backlinks3():
    ref = """# ID2 Mathematics
# Backlinks
- [[ID0 Index]]"""
    s = '\n'.join(md_files.md_files['ID2 Mathematics'].content)
    assert ref==s