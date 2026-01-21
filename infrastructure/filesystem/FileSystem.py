from pathlib import Path

class FileSystem:
    def is_file(self, file: str) -> bool:
        return Path(file).is_file()
    
    def delete(self, file: str) -> None:
        input_file = Path(file)
        if input_file.is_file():
            input_file.unlink()
