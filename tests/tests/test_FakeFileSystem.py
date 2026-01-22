import pytest

from tests import FakeFileSystem

def test_FakeFileSystem_helpers():
    fs = FakeFileSystem()
    existing_file = "/fake/file.mp4"
    non_existing_file = "/fake/file2.mp4"
    existing_dir = "/fake/dir"
    non_existing_dir = "/fake/dir2"

    fs.add(existing_file)
    fs.add(existing_dir, is_dir=True)

    assert fs._exists(existing_file) == True
    assert fs._exists(non_existing_file) == False
    assert fs._exists(existing_dir) == True
    assert fs._exists(non_existing_dir) == False

    assert fs.is_file(existing_file) == True
    assert fs.is_file(non_existing_file) == False
    assert fs.is_file(existing_dir) == False
    assert fs.is_file(non_existing_dir) == False

    assert fs._is_dir(existing_file) == False
    assert fs._is_dir(non_existing_file) == False
    assert fs._is_dir(existing_dir) == True
    assert fs._is_dir(non_existing_dir) == False

def test_FakeFileSystem_add():
    fs = FakeFileSystem()
    existing_file = "/fake/file.mp4"
    existing_dir = "/fake/dir"
    # mirror current inode
    inode = int(fs._next_inode)

    # Test add works as expected on file
    fs.add(existing_file)
    assert fs.is_file(existing_file)
    assert fs._files[existing_file] == inode
    assert fs._link_count[inode] == 1

    inode += 1
    # Test fs._next_inode incrementing correctly
    assert inode == fs._next_inode

    # Test add works as expected on directory
    fs.add(existing_dir, is_dir=True)
    assert fs._is_dir(existing_dir)
    assert fs._dirs[existing_dir] == inode
    assert fs._link_count[inode] == 1

    # Test adding already existing file/ dir raises error correctly
    with pytest.raises(FileExistsError):
        fs.add(existing_file)
        fs.add(existing_dir, is_dir=True)

def test_FakeFileSystem_inode():
    fs = FakeFileSystem()
    existing_file = "/fake/file.mp4"
    existing_dir = "/fake/dir"

    fs.add(existing_file)
    fs.add(existing_dir, is_dir=True)

    file_inode = fs._inode(existing_file)
    dir_inode = fs._inode(existing_dir)

    assert file_inode == fs._files[existing_file]
    assert dir_inode == fs._dirs[existing_dir]

def test_FakeFileSystem_inode_for():
    fs = FakeFileSystem()
    existing_file = "/fake/file.mp4"
    non_existing_file = "/fake/file2.mp4"
    existing_dir = "/fake/dir"
    non_existing_dir = "/fake/dir2"

    fs.add(existing_file)
    fs.add(existing_dir, is_dir=True)

    assert fs._inode_for(existing_file) == (fs._files[existing_file], False)
    assert fs._inode_for(existing_dir) == (fs._dirs[existing_dir], True)

    # Check errors raised correctly
    with pytest.raises(FileNotFoundError):
        fs._inode_for(non_existing_file)
        fs._inode_for(non_existing_dir)

def test_FakeFileSystem_hardlink():
    fs = FakeFileSystem()
    existing_file = "/fake/file.mp4"
    non_existing_file = "/fake/file2.mp4"
    destination_hardlink = "/fake/file3.mp4"
    existing_dir = "/fake/dir"

    fs.add(existing_file)
    fs.add(existing_dir, is_dir=True)

    # Test hardlink works as expected
    fs.hardlink(existing_file, destination_hardlink)
    assert fs._inode(existing_file) == fs._inode(destination_hardlink)
    inode = fs._inode(destination_hardlink)
    assert fs._link_count[inode] == 2

    # Test source is a directory error
    with pytest.raises(IsADirectoryError):
        fs.hardlink(existing_dir, non_existing_file)

    # Test destination is a directory error
    with pytest.raises(NotImplementedError):
        fs.hardlink(existing_file, existing_dir)

    # Test destination already exists error
    with pytest.raises(FileExistsError):
        fs.hardlink(existing_file, existing_file)

def test_FakeFileSystem_delete():
    fs = FakeFileSystem()
    existing_file = "/fake/file.mp4"
    non_existing_file = "/fake/file2.mp4"
    existing_dir = "/fake/dir"
    non_existing_dir = "fake/dir2"

    fs.add(existing_file)
    fs.add(existing_dir, is_dir=True)

    # Test file deletion works correctly

    fs.delete(existing_file)
    assert existing_file not in fs._files

    # Test dir deletion works correctly

    fs.delete(existing_dir)
    assert existing_dir not in fs._dirs

    # Test failure conditions
    with pytest.raises(FileNotFoundError):
        fs.delete(non_existing_file)
        fs.delete(non_existing_dir)

def test_FakeFilsystem_delete_with_hardlinked_file():
    fs = FakeFileSystem()
    existing_file = "/fake/file.mp4"
    destination_hardlink = "/fake/file3.mp4"

    fs.add(existing_file)
    fs.hardlink(existing_file, destination_hardlink)
    
    assert fs._link_count[fs._files[destination_hardlink]] == 2

    fs.delete(existing_file)
    assert fs._link_count[fs._files[destination_hardlink]] == 1

