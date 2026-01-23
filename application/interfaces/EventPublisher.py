from typing import (
    Protocol,
    TypeVar,
    Iterable,
)

from domain import (
    Event,
    OperationContext,
)

from application import EventEnvelope

E = TypeVar("E", bound=Event)

class EventPublisher(Protocol):

    def create_envelope(self, event: Event, operation_context: OperationContext) -> EventEnvelope:
        ...

    def publish(self, event: Event, operation_context: OperationContext) -> None:
        ...

    def publish_all(self, events: Iterable[Event], operation_context: OperationContext) -> None:
        ...