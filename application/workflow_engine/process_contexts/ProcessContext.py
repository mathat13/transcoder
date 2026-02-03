from uuid import UUID
from dataclasses import dataclass

from application import (
      EventEnvelope,
)

@dataclass(frozen=True)
class ProcessContext:
    operation_id: UUID
    envelope: EventEnvelope