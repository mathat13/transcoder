from pathlib import Path

from domain import FileInfo

class FileSystem:
    def exists(self, file: FileInfo) -> bool:
        return Path(file.path).exists()
