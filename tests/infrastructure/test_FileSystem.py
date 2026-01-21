import pytest

from infrastructure import FileSystem

def test_filesystem_exists_returns_true_for_existing_file(tmp_path):
    fs = FileSystem()

    file_path = tmp_path / "output.mp4"
    file_path.write_text("fake data")

    result = fs.exists(file_path)

    # Assert
    assert result is True

def test_filesystem_exists_returns_false_for_non_existing_file(tmp_path):
    fs = FileSystem()

    file_path  = tmp_path / "non_existing.mp4"

    # Don't actually write file

    result = fs.exists(file_path)

    assert result is False