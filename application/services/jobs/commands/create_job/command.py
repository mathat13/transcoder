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
    def from_source_file(cls,
                    source_file: FileInfo
                    ) -> "CreateJobCommand":
        return cls(
            source_file=source_file,
        )
    
    @classmethod
    def from_source_file_and_media_ids(cls,
                    source_file: FileInfo,
                    media_ids: ExternalMediaIDs
                    ) -> "CreateJobCommand":
        return cls(
            source_file=source_file,
            media_ids=media_ids,
        )

