from pathlib import Path

class FileSystem:
    def exists(self, file: str) -> bool:
        return Path(file).exists()
