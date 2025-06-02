import sys
import shutil
import pytest
import runpy
from pathlib import Path
from ..scripts.update_index import (
    main
)

@pytest.fixture
def setup_for_main():
    path = Path("temp")
    path_group1 = Path("temp/group1")
    path_group1.mkdir(parents=True, exist_ok=True)
    path_group2 = Path("temp/group2")
    path_group2.mkdir(parents=True, exist_ok=True)
    path_group3 = Path("temp/group3")
    path_group3.mkdir(parents=True, exist_ok=True)

    filenames = ["No Such Thing [Chris Cornell].mp3", "The Pot [TOOL].mp3",
                  "Black [Pearl Jam].mp3"]
    for filename in filenames:
        with open("temp/group1/"+filename, 'w') as file:
            pass

    filenames = ["Who Knows [Marion Black].mp3", "Sixteen Tons.mp3",
                  "Autumn Leaves.mp3"]
    for filename in filenames:
        with open("temp/group2/"+filename, 'w') as file:
            pass

    filenames = ["Help! [Beatles].mp3", "Nowhere Man [Beatles].mp3"]
    for filename in filenames:
        with open("temp/group3/"+filename, 'w') as file:
            pass

    yield path
    #time.sleep(2)
    shutil.rmtree("temp")

def test_main_folders(setup_for_main):
    main(setup_for_main)
    assert Path("temp").is_dir() == True and Path("temp/Beatles (2)").is_dir() == True and Path("temp/Chris Cornell (1)").is_dir() == True
    assert Path("temp/Marion Black (1)").is_dir() == True  and Path("temp/Pearl Jam (1)").is_dir() == True  and Path("temp/Tool (1)").is_dir() == True
    assert Path("temp/VA (2)").is_dir() == True

def test_main_files(setup_for_main):
    main(setup_for_main)
    assert Path("temp/Beatles (2)/Help! [Beatles].mp3").is_file() == True and Path("temp/Beatles (2)/Nowhere Man [Beatles].mp3").is_file() == True
    assert Path("temp/Chris Cornell (1)/No Such Thing [Chris Cornell].mp3").is_file() == True
    assert Path("temp/Marion Black (1)/Who Knows [Marion Black].mp3").is_file() == True
    assert Path("temp/Pearl Jam (1)/Black [Pearl Jam].mp3").is_file() == True
    assert Path("temp/Tool (1)/The Pot [Tool].mp3").is_file() == True
    assert Path("temp/VA (2)/Autumn Leaves.mp3").is_file() == True and Path("temp/VA (2)/Sixteen Tons.mp3").is_file() == True

def test_console_start(setup_for_main):
    arguments = ["temp"]
    original_argv = sys.argv
    sys.argv = [sys.argv[0]] + arguments
    runpy.run_path("hse-tp-02-Elvira0608/src/scripts/update_index.py", run_name="__main__")
    sys.argv = original_argv