from typing import (
    Iterable,
    Callable,
    Type,
    DefaultDict,
    List,
)

from application import (
    EnvelopeTransportCapable,
    EventEnvelope,
    Event,
)

from collections import defaultdict

class FakeSyncEventBus(EnvelopeTransportCapable):
    def __init__(self):
        self.subscribers: DefaultDict[Type[Event], List[Callable[[EventEnvelope], None]]] = defaultdict(list)
        self.published: List[Type[Event]] = []
        self.unpublished: List[Type[Event]] = []

    def subscribe(self, event_type: Type[Event], handler: Callable[[EventEnvelope], None]):
        self.subscribers[event_type].append(handler)

    def publish(self, envelope: EventEnvelope):
        event = envelope.event

        if not self.subscribers:
            self.unpublished.append(type(envelope.event))
            return

        self.published.append(type(envelope.event))
        for handler in self.subscribers[type(event)]:
            handler(envelope)

    def publish_all(self, envelopes: Iterable[EventEnvelope]):
        for envelope in envelopes:
            self.publish(envelope)