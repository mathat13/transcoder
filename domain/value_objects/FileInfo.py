from pathlib import Path
from dataclasses import dataclass
from typing import Union

@dataclass(frozen=True)
class FileInfo:
    path: Path
    
    @property
    def parent(self) -> Path:
        return self.path.parent

    @property
    def name(self) -> str:
        return self.path.name

    @property
    def extension(self) -> str:
        return self.path.suffix
    
    @classmethod
    def from_path(cls, path: Union[str, Path]) -> "FileInfo":
        return cls(
            path=Path(path)
        )
    
    @classmethod
    def from_parent_and_name(cls, parent: Path, name: str) -> "FileInfo":
        return cls(
            path=Path(parent / name)
        )