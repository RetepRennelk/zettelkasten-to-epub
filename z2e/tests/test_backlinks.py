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
- [[ID4 This zettel links to an image]]
- [[ID5 This zettel embeds an image]]
## Backlinks
None"""
    s = '\n'.join(files.get_content('ID0 Index'))
    assert ref==s

def test_backlinks2():
    ref = """# ID1 Zettelkasten
## Metadata

## Notes
- [[ID1A Origin of the Zettelkasten]]
## Backlinks
- [[ID0 Index]]"""
    s = '\n'.join(files.get_content('ID1 Zettelkasten'))
    print(s)
    assert ref==s

def test_backlinks3():
    ref = """# ID2 Mathematics
## Metadata

## Notes
## Backlinks
- [[ID0 Index]]"""
    s = '\n'.join(files.get_content('ID2 Mathematics'))
    assert ref==s