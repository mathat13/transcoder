
from dataclasses import dataclass
from uuid import UUID

from domain import (
    Event,
    OperationContext,
)

@dataclass(frozen=True)
class EventEnvelope:
    event: Event
    operation_id: UUID

    @classmethod
    def create(cls, event: Event, context: OperationContext) -> "EventEnvelope":
        return cls(
            event=event,
            operation_id=context.operation_id,
        )
