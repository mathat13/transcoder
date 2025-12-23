import os
from dataclasses import dataclass

@dataclass(frozen=True)
class FileInfo:
    path: str

    def __post_init__(self):
        self.validate()

    def validate(self):
        if not self.path or "/" not in self.path:
            raise ValueError("Invalid file path format.")
    
    @property
    def parent(self) -> str:
        return os.path.dirname(self.path)

    @property
    def name(self) -> str:
        return os.path.basename(self.path)

    @property
    def extension(self) -> str:
        return os.path.splitext(self.path)[1]
    
    @property
    def transcode_file(self) -> "FileInfo":
        base, ext = os.path.splitext(self.path)
        return FileInfo(f"{base}_transcoded{ext}")