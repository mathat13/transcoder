from domain import FileInfo

class FakeFileSystem:
    def __init__(self):
        self._files: set[str] = set()

    def add(self, file: FileInfo) -> None:
        self._files.add(file.path)

    def exists(self, file: FileInfo) -> bool:
        return file.path in self._files
