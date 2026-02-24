from typing import Optional
from dataclasses import dataclass

from domain import FileInfo

@dataclass(frozen=True)
class FileContext:
    source_file: Optional[FileInfo] = None
    transcode_file: Optional[FileInfo] = None