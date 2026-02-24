import pytest
from pathlib import Path

from application import (
    FileSystemDestinationExistsButDifferentFile,
    FileSystemSourceFileIsDirectory,
    FileSystemFileMissing,
    FileSystemIOError,
    RetryableException,
    TerminalException,
)
from infrastructure import FileSystem

def test_FileSystem_assert_file_exists_raises_exception_on_failure(tmp_path: Path):
    fs = FileSystem()

    file_path  = tmp_path / "non_existing.mp4"

    # Don't actually write file
    with pytest.raises(FileSystemFileMissing) as exc:
        fs.assert_file_existence(file_path.as_posix())

    exception = exc.value
    assert exception.file.path == str(file_path)

def test_FileSystem_assert_file_exists_returns_None_on_success(tmp_path: Path):
    fs = FileSystem()

    file_path = tmp_path / "output.mp4"
    file_path.write_text("fake data")

    # Should not raise
    result = fs.assert_file_existence(file_path.as_posix())

    assert result is None


def test_FileSystem_delete_removes_existing_file(tmp_path: Path):
    fs = FileSystem()

    file_path = tmp_path / "output.mp4"
    file_path.write_text("fake data")

    fs.delete(file_path.as_posix())

    with pytest.raises(FileSystemFileMissing):
        fs.assert_file_existence(file_path.as_posix())


def test_FileSystem_delete_returns_None_on_non_existing_file(tmp_path: Path):
    fs = FileSystem()

    file_path = tmp_path / "output.mp4"

    fs.delete(file_path.as_posix())

    with pytest.raises(FileSystemFileMissing):
        fs.assert_file_existence(file_path.as_posix())

def test_FileSystem_delete_raises_SourceFileIsDirectory_correctly(tmp_path: Path):
    fs = FileSystem()

    dir_path = tmp_path / "temp_dir"
    dir_path.mkdir()

    with pytest.raises(FileSystemSourceFileIsDirectory) as exc:
        fs.delete(dir_path.as_posix())
    
    exception = exc.value
    assert exception.operation == "delete"
    assert exception.file.path == str(dir_path)
    assert isinstance(exception, TerminalException)

def test_FileSystem_delete_raises_FileSystemIOError_on_OSError(monkeypatch):
    fs = FileSystem()
    test_path = "/tmp/somefile"

    def fake_unlink(self):
        raise OSError("permission denied")

    monkeypatch.setattr(Path, "unlink", fake_unlink)
    monkeypatch.setattr(Path, "exists", lambda self: True)
    monkeypatch.setattr(Path, "is_dir", lambda self: False)

    with pytest.raises(FileSystemIOError) as exc:
        fs.delete(test_path)

    exception = exc.value
    assert exception.operation == "delete"
    assert exception.file.path == str(test_path)
    assert isinstance(exception.original, OSError)
    assert isinstance(exception, RetryableException)

def test_FileSystem_hardlink_creates_hardlink(tmp_path: Path):
    fs = FileSystem()

    source_file = tmp_path / "original.txt"
    source_file.write_text("fake data")

    dest = tmp_path / "hardlink.txt"

    fs.hardlink(source_file.as_posix(), dest.as_posix())

    fs.assert_file_existence(dest.as_posix())

    assert Path(source_file).stat().st_ino == Path(dest).stat().st_ino

def test_FileSystem_hardlink_appends_source_file_name_to_dest_if_dest_is_existing_directory(tmp_path: Path):
    fs = FileSystem()

    src_file_name = "original.txt"

    source_file = tmp_path / src_file_name
    source_file.write_text("fake data")

    dest = tmp_path / "subdir"
    dest.mkdir()

    fs.hardlink(source_file.as_posix(), dest.as_posix())

    output_file = tmp_path / dest / src_file_name

    fs.assert_file_existence(output_file.as_posix())

    assert Path(output_file).stat().st_ino == Path(source_file).stat().st_ino

def test_FileSystem_hardlink_raises_SourceFileIsDirectory_correctly(tmp_path: Path):
    fs = FileSystem()

    source_directory = tmp_path / "directory"
    source_directory.mkdir()

    dest = tmp_path / "hardlink.txt"

    with pytest.raises(FileSystemSourceFileIsDirectory) as exc:
        fs.hardlink(source_directory.as_posix(), dest.as_posix())

    exception = exc.value
    assert exception.operation == "hardlink"
    assert exception.file.path == str(source_directory)
    assert isinstance(exception, TerminalException)

def test_FileSystem_hardlink_raises_DestinationExistsButDifferentFile_correctly(tmp_path: Path):
    fs = FileSystem()

    source_file = tmp_path / "original.txt"
    source_file.write_text("fake data")

    dest = tmp_path / "different_file.txt"
    dest.write_text("more fake data")

    with pytest.raises(FileSystemDestinationExistsButDifferentFile) as exc:
        fs.hardlink(source_file.as_posix(), dest.as_posix())

    exception = exc.value
    assert exception.file.path == str(dest)
    assert isinstance(exception, TerminalException)

def test_FileSystem_hardlink_raises_SourceFileMissing_correctly(tmp_path: Path):
    fs = FileSystem()

    src_file_name = "original.txt"
    source_file = tmp_path / src_file_name

    dest = tmp_path / "hardlink.txt"

    with pytest.raises(FileSystemFileMissing) as exc:
        fs.hardlink(source_file.as_posix(), dest.as_posix())

    exception = exc.value
    assert exception.file.path == str(source_file)
    assert isinstance(exception, TerminalException)

def test_FileSystem_hardlink_raises_FileSystemIOError_on_OSError_with_failed_hardlink_attempt(monkeypatch):
    fs = FileSystem()
    test_path = "/tmp/somefile.txt"
    destination = "/tmp/someotherfile.txt"

    def fake_hardlink_to(self, target: Path):
        raise OSError("permission denied")

    monkeypatch.setattr(Path, "hardlink_to", fake_hardlink_to)
    monkeypatch.setattr(Path, "exists", lambda self: False)
    monkeypatch.setattr(Path, "is_dir", lambda self: False)
    monkeypatch.setattr(Path, "is_file", lambda self: True)

    with pytest.raises(FileSystemIOError) as exc:
        fs.hardlink(test_path, destination)

    exception = exc.value
    assert exception.operation == "hardlink"
    assert exception.file.path == str(destination)
    assert isinstance(exception.original, OSError)
    assert isinstance(exception, RetryableException)