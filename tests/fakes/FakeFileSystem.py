from domain import FileInfo

class FakeFileSystem:
    def __init__(self):
        self._files: set[str] = set()

    def add(self, file: str) -> None:
        self._files.add(file)

    def exists(self, file: str) -> bool:
        return file in self._files
