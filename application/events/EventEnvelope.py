
from dataclasses import dataclass

from domain import (
    Event,
    OperationContext,
)

@dataclass(frozen=True)
class EventEnvelope:
    event: Event
    context: OperationContext

    @classmethod
    def create(cls, event: Event, context: OperationContext) -> "EventEnvelope":
        return cls(
            event=event,
            context=context,
        )
