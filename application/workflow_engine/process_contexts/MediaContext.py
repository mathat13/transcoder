from dataclasses import dataclass

from domain import ExternalMediaIDs

@dataclass(frozen=True)
class MediaContext:
    media_ids: ExternalMediaIDs