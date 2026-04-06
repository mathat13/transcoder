from typing import Optional
from dataclasses import dataclass

from domain import FileInfo

@dataclass(frozen=True)
class FileContext:
    source_file: Optional[FileInfo] = None
    transcode_output_file: Optional[FileInfo] = None
    delivery_file: Optional[FileInfo] = None