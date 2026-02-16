from typing import (
    Protocol,
    Callable,
    Type,
    Iterable,
)

from application.events.EventEnvelope import EventEnvelope

from domain import Event

class EnvelopeTransportCapable(Protocol):
    def subscribe(self, event_type: Type[Event], handler: Callable[[EventEnvelope], None]) -> None:
        ...

    def publish(self, envelope: EventEnvelope) -> None:
        ...

    def publish_all(self, envelopes: Iterable[EventEnvelope]) -> None:
        ...