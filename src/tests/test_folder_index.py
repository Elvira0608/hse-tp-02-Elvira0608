import shutil
import pytest
import time
from pathlib import Path
from ..media_indexing.folder_index import (
    apply_new_media_paths,
    get_folders,
    get_folder_files,
    get_updated_media_paths,
    reindex_folders,
    get_artist,
    remove_counter,
    remove_artist,
    Folder,
    Media
)

def test_get_artist_right_artist():
    impliedString = "Black Sabbath"
    assert get_artist("song1 [Black Sabbath].mp3") == impliedString

def test_get_artist_wrong_artist():
    impliedString = "Black Sabbath"
    assert get_artist("song1 [Metallica].mp3") != impliedString

def test_get_artist_no_artist():
    assert get_artist("song1.mp3") == None  

def test_get_artist_exception():
    with pytest.raises(Exception) as e_info:
        get_artist("song1 [Black Sabbath][Metallica].mp3")
    assert str(e_info.value) == "Got more than one artist in a string: song1 [Black Sabbath][Metallica].mp3"

def test_remove_counter():
    impliedString = "Artist A"
    assert remove_counter("Artist A (2)") == impliedString

#-----------------Тестирование с одним медиафайлом с указанием исполнителя---------------------------

@pytest.fixture
def create_folders_and_media_files():
    folder_path = Path("temp")
    path = Path("temp/inner")
    path.mkdir(parents=True, exist_ok=True)
    file = open("temp/inner/song [Metallica].mp3", "w")
    file.close()
    folder = Folder(path)
    yield folder, folder_path, path
    #time.sleep(2)
    shutil.rmtree("temp")

def test_get_folders_on_empty_path(tmp_path):
    assert get_folders(tmp_path) == []

# тест не проходится из-за невозможности сравнения объектов класса Folder
def test_get_folders(create_folders_and_media_files):
    assert get_folders(Path("temp")) == [create_folders_and_media_files[0]]


def test_get_folder_files_on_empty(tmp_path):
    assert get_folder_files(tmp_path) == []

def test_get_folder_files(create_folders_and_media_files):
    print(get_folder_files(create_folders_and_media_files[2]))
    assert get_folder_files(create_folders_and_media_files[2]) == [Path("temp/inner/song [Metallica].mp3")]

def test_get_updated_media_paths_on_empty(tmp_path):
   assert get_updated_media_paths(tmp_path) == {}


def test_get_updated_media_paths(create_folders_and_media_files):
    assert get_updated_media_paths(create_folders_and_media_files[1]) == {Path("temp/inner/song [Metallica].mp3"):Path("temp/Metallica/song [Metallica].mp3")}

def test_apply_new_media_paths(create_folders_and_media_files):
    mapping = get_updated_media_paths(create_folders_and_media_files[1])
    assert apply_new_media_paths(mapping) == None and Path("temp/Metallica").is_dir() == True and Path("temp/Metallica/song [Metallica].mp3").is_file() == True

def test_reindex_folders(create_folders_and_media_files):
    mapping = get_updated_media_paths(create_folders_and_media_files[1])
    apply_new_media_paths(mapping)
    assert reindex_folders(get_folders(create_folders_and_media_files[1])) == None and Path("temp/Metallica (1)").is_dir() == True


def test_get_media_list(create_folders_and_media_files):
    folder = create_folders_and_media_files[0]
    assert folder.get_media_list() != []

def test_get_media_counter(create_folders_and_media_files):
    folder = create_folders_and_media_files[0]
    assert folder.get_counter() == 1

def test_get_new_folder_name (create_folders_and_media_files):
    folder = create_folders_and_media_files[0]
    assert folder.get_new_folder_name() == "inner (1)"
    mapping = get_updated_media_paths(create_folders_and_media_files[1])
    apply_new_media_paths(mapping)
    folder = Folder(Path("temp/Metallica"))
    print(folder.get_new_folder_name())
    assert folder.get_new_folder_name() == "Metallica (1)"

def test_rename_with_counter(create_folders_and_media_files):
    folder = create_folders_and_media_files[0]
    assert folder.rename_with_counter() == None and Path("temp/inner (1)").is_dir()

def test_create_folder(create_folders_and_media_files):
    with pytest.raises(Exception) as e_info:
        Folder(Path("temp/Metallica/song [Metallica].mp3"))
    assert str(e_info.value) == "temp\Metallica\song [Metallica].mp3 is not a dir, but its expected to be"

def test_create_media(create_folders_and_media_files):
    print(Path("temp/inner").is_dir())
    with pytest.raises(Exception) as e_info:
        Media(Path("temp/inner"))
    assert str(e_info.value) == "temp\inner is a dir, but its expected to be"

def test_rename_update(create_folders_and_media_files):
    media = Media(Path("temp/inner/song [Metallica].mp3"))
    media.rename_update()
    assert Path("temp\inner\song [Metallica].mp3").is_file() == True

def test_remove_artist():
    assert remove_artist("song [Metallica].mp3") == "song .mp3"