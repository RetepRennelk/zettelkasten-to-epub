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

def test_id0_index():
    id0_index = """# ID0 Index

- [[ID1 Zettelkasten]]
- [[ID2 Mathematics]]""".split('\n')
    md_file = md_files.md_files['ID0 Index']

    for x, y in zip(md_file.content, id0_index):
        assert x==y

    out_links = [x.name for x in md_file.get_outgoing_links()]
    assert len(out_links) == 2

    assert "ID1 Zettelkasten" in out_links
    assert "ID2 Mathematics" in out_links

def test_md_files_incoming_links():
    inc_links = md_files.get_incoming_links("ID0 Index")
    assert len(inc_links) == 0
    inc_links = md_files.get_incoming_links("ID1 Zettelkasten")
    assert len(inc_links)==1
    assert inc_links[0].name=="ID0 Index"
    inc_links = md_files.get_incoming_links("ID2 Mathematics")
    assert len(inc_links)==1
    assert inc_links[0].name=="ID0 Index"