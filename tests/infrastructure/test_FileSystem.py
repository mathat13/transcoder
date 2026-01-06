import pytest

from infrastructure import FileSystem
from domain import FileInfo

def test_filesystem_exists_returns_true_for_existing_file(tmp_path):
    fs = FileSystem()

    file_path = tmp_path / "output.mp4"
    file_path.write_text("fake data")

    file_info = FileInfo(str(file_path))

    result = fs.exists(file_info)

    # Assert
    assert result is True

def test_filesystem_exists_returns_false_for_non_existing_file(tmp_path):
    fs = FileSystem()

    file_path  = tmp_path / "non_existing.mp4"

    # Don't actually write file

    file_info = FileInfo(str(file_path))

    result = fs.exists(file_info)

    assert result is False