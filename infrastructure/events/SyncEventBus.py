from collections import defaultdict
from typing import (
    Callable,
    Type,
    Iterable,
    List,
    DefaultDict,
)

from domain import (
    Event,
)

from application import (
    EventEnvelope,
    EnvelopeTransportCapable,
)

class SyncEventBus(EnvelopeTransportCapable):
    _subscribers: DefaultDict[Type[Event], List[Callable[[EventEnvelope], None]]] = defaultdict(list)

    def subscribe(self, event_type: Type[Event], handler: Callable[[EventEnvelope], None]):
        self._subscribers[event_type].append(handler)

    def publish(self, envelope: EventEnvelope):
        event = envelope.event
        if event.__class__ not in self._subscribers:
            return
        for handler in self._subscribers[type(event)]:
            handler(envelope)

    def publish_all(self, envelopes: Iterable[EventEnvelope]):
        for envelope in envelopes:
            self.publish(envelope)