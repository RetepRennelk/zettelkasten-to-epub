from z2e.src.wikilinks import MD_Files
import pytest

folder_path = './NoNotes'

def test_exit():
    with pytest.raises(SystemExit) as e:
        md_files = MD_Files(folder_path)
    assert e.type == SystemExit
    assert e.value.code == 0