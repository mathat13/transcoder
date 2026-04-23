from dataclasses import dataclass

from domain import (
    FileInfo,
    ExternalMediaIDs,
)
@dataclass
class CreateJobCommand:
    source_file: FileInfo
    media_ids: ExternalMediaIDs | None = None

    @classmethod
    def from_manual(cls, source_file: str) -> "CreateJobCommand":
        return cls(
            source_file=FileInfo.from_path(source_file),
        )
    
    @classmethod
    def from_radarr(cls, source_file: str, media_id: int) -> "CreateJobCommand":
        return cls(
            source_file=FileInfo.from_path(source_file),
            media_ids=ExternalMediaIDs.from_radarr(media_id),
        )

