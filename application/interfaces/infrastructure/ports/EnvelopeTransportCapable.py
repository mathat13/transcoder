from typing import (
    Protocol,
    Callable,
    Type,
    Iterable,
)

from domain import Event

from application import EventEnvelope

class EnvelopeTransportCapable(Protocol):
    def subscribe(self, event_type: Type[Event], handler: Callable[[EventEnvelope], None]) -> None:
        ...

    def publish(self, envelope: EventEnvelope) -> None:
        ...

    def publish_all(self, envelopes: Iterable[EventEnvelope]) -> None:
        ...