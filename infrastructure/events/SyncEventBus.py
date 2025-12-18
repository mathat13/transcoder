from collections import defaultdict
from typing import (
    Callable,
    TypeVar,
    Type,
    Iterable,
)

from domain import Event

E = TypeVar("E", bound=Event)

class SyncEventBus:
    def __init__(self):
        self._subscribers = defaultdict(list)

    def subscribe(self, event_type: Type[E], handler: Callable[[E], None]):
        self._subscribers[event_type].append(handler)

    def publish(self, event: Event):
        if event.__class__ not in self._subscribers:
            return
        for handler in self._subscribers[type(event)]:
            handler(event)

    def publish_all(self, events: Iterable[Event]):
        for event in events:
            self.publish(event)