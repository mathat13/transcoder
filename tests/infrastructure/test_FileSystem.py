import pytest

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

def test_Fiesystem_delete_does_not_delete_directory(tmp_path):
    fs = FileSystem()

    dir_path = tmp_path / "temp_dir"
    dir_path.mkdir()

    fs.delete(dir_path)

    result = fs.is_file(dir_path)

    assert result is False

