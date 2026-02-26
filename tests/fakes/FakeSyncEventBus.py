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
        self._subscribers: DefaultDict[Type[Event], List[Callable[[EventEnvelope], None]]] = defaultdict(list)
        self._processed: List[EventEnvelope] = []
        self._published: List[EventEnvelope] = []
        self._unpublished: List[EventEnvelope] = []

    # Helpers
    # Returns publish order instead of order of execution
    @property
    def published_event_types(self) -> list[type[Event]]:
        return [type(envelope.event) for envelope in self._published]

    @property
    def unpublished_event_types(self) -> list[type[Event]]:
        return [type(envelope.event) for envelope in self._unpublished]

    @property
    def processed_event_types(self) -> list[type[Event]]:
        return [type(envelope.event) for envelope in self._processed]

    # Protocol
    def subscribe(self, event_type: Type[Event], handler: Callable[[EventEnvelope], None]):
        self._subscribers[event_type].append(handler)

    def publish(self, envelope: EventEnvelope):
        event = envelope.event
        self._processed.append(envelope)

        if event.__class__ not in self._subscribers:
            self._unpublished.append(envelope)
            return

        self._published.append(envelope)
        for handler in self._subscribers[type(event)]:
            handler(envelope)

    def publish_all(self, envelopes: Iterable[EventEnvelope]):
        for envelope in envelopes:
            self.publish(envelope)