import pytest
from pathlib import Path

from infrastructure import FileSystem

def test_filesystem_is_file_returns_true_for_existing_file(tmp_path):
    fs = FileSystem()

    file_path = tmp_path / "output.mp4"
    file_path.write_text("fake data")

    result = fs.is_file(file_path)

    # Assert
    assert result is True

def test_filesystem_is_file_returns_false_for_non_existing_file(tmp_path):
    fs = FileSystem()

    file_path  = tmp_path / "non_existing.mp4"

    # Don't actually write file

    result = fs.is_file(file_path)

    assert result is False

def test_FileSystem_delete_removes_existing_file(tmp_path):
    fs = FileSystem()

    file_path = tmp_path / "output.mp4"
    file_path.write_text("fake data")

    fs.delete(file_path)

    result = fs.is_file(file_path)

    assert result is False

def test_FileSystem_delete_silently_removes_non_existing_file(tmp_path):
    fs = FileSystem()

    file_path = tmp_path / "output.mp4"

    fs.delete(file_path)

    result = fs.is_file(file_path)

    assert result is False

def test_Filesystem_delete_does_not_delete_directory(tmp_path):
    fs = FileSystem()

    dir_path = tmp_path / "temp_dir"
    dir_path.mkdir()

    fs.delete(dir_path)

    result = fs.is_file(dir_path)

    assert result is False

def test_FileSystem_hardlink_creates_hardlink(tmp_path):
    fs = FileSystem()

    source_file = tmp_path / "original.txt"
    source_file.write_text("fake data")

    dest = tmp_path / "hardlink.txt"

    fs.hardlink(source_file, dest)

    assert fs.is_file(dest)
    assert Path(source_file).stat().st_ino == Path(dest).stat().st_ino

def test_FileSystem_hardlink_appends_source_file_name_to_dest_if_dest_is_existing_directory(tmp_path):
    fs = FileSystem()

    src_file_name = "original.txt"

    source_file = tmp_path / src_file_name
    source_file.write_text("fake data")

    dest = tmp_path / "subdir"
    dest.mkdir()

    fs.hardlink(source_file, dest)

    output_file = tmp_path / dest / src_file_name

    assert fs.is_file(output_file)
    assert Path(output_file).stat().st_ino == Path(source_file).stat().st_ino

def test_FileSystem_returns_error_when_source_file_does_not_exist(tmp_path):
    fs = FileSystem()

    src_file_name = "original.txt"

    source_file = tmp_path / src_file_name

    dest = tmp_path / "subdir"

    with pytest.raises(ValueError):
        fs.hardlink(source_file, dest)




