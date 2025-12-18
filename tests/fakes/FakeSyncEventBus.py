from typing import (
    Callable,
    TypeVar,
    Type,
    Iterable,
)

from domain import Event

E = TypeVar("E", bound=Event)

class FakeSyncEventBus:
    def __init__(self):
        self.subscribers = {}
        self.published = []

    def subscribe(self, event_type: Type[E], handler: Callable[[E], None]):
        self.subscribers.setdefault(event_type, []).append(handler)

    def publish(self, event: Event):
        if not self.subscribers:
            return

        self.published.append(event)
        for handler in self.subscribers[type(event)]:
            handler(event)

    def publish_all(self, events: Iterable[Event]):
        for evt in events:
            self.publish(evt)