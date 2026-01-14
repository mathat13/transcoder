from typing import (
    Callable,
    TypeVar,
    Type,
    Iterable,
)

from application import EventEnvelope

class FakeSyncEventBus:
    def __init__(self):
        self.subscribers = {}
        self.published = []

    def subscribe(self, event_type, handler):
        self.subscribers.setdefault(event_type, []).append(handler)

    def publish(self, envelope: EventEnvelope):
        event = envelope.event

        if not self.subscribers:
            return

        self.published.append(envelope)
        for handler in self.subscribers[type(event)]:
            handler(envelope)

    def publish_all(self, envelopes: Iterable[EventEnvelope]):
        for envelope in envelopes:
            self.publish(envelope)