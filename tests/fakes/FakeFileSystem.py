class FakeFileSystem:
    def __init__(self):
        self._files: set[str] = set()

    def add(self, file: str) -> None:
        self._files.add(file)

    def is_file(self, file: str) -> bool:
        return file in self._files
    
    def delete(self, file: str) -> None:
        if self.is_file(file):
            self._files.remove(file)
