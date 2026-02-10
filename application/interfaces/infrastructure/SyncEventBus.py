from typing import (
    Protocol,
    Callable,
    TypeVar,
    Type,
    Iterable,
)

from domain import Event

from application import EventEnvelope

E = TypeVar("E", bound=Event)

class SyncEventBus(Protocol):
    def subscribe(self, event_type: Type[E], handler: Callable[[E], None]) -> None:
        ...

    def publish(self, event: EventEnvelope) -> None:
        ...

    def publish_all(self, events: Iterable[EventEnvelope]) -> None:
        ...