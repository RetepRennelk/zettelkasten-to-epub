from z2e.src.wikilinks import Files
from glob import glob

dirs = dict(
    notes='./Notes',
    assets='./Assets')
files = Files(dirs)

def test_backlinks1():
    ref = """# ID0 Index

- [[ID1 Zettelkasten]]
- [[ID2 Mathematics]]
- [[ID3 A note that doesn't exist]]
## Backlinks
None"""
    s = '\n'.join(files.get_content('ID0 Index'))
    assert ref==s

def test_backlinks2():
    ref = """# ID1 Zettelkasten

A Zettelkasten note
## Backlinks
- [[ID0 Index]]"""
    s = '\n'.join(files.get_content('ID1 Zettelkasten'))
    print(s)
    assert ref==s

def test_backlinks3():
    ref = """# ID2 Mathematics
## Backlinks
- [[ID0 Index]]"""
    s = '\n'.join(files.get_content('ID2 Mathematics'))
    assert ref==s