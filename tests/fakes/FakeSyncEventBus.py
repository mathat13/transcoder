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
    def _envelopes_of_event_type(
    self,
    envelopes: list[EventEnvelope],
    event_type: type[Event] | tuple[type[Event], ...] | None,
    ) -> list[EventEnvelope]:
        """
        Returns a list of envelopes with matching event type.
        """
        if event_type is None:
            return list(envelopes)
        return [
            envelope
            for envelope in envelopes
            if isinstance(envelope.event, event_type)
        ]
    
    def _envelopes_to_events(self, envelopes: List[EventEnvelope]) -> List[Event]:
        """
        Converts a list of EventEnvelopes into a list of Events.
        """
        return [
            envelope.event
            for envelope in envelopes
        ]
    
    def _envelopes_to_event_types(self, envelopes: List[EventEnvelope]) -> List[Type[Event]]:
        """
        Converts a list of EventEnvelopes into a list of Event types.
        """
        return [
            type(envelope.event)
            for envelope in envelopes
        ]

    # Queries
    # Envelope lists
    def processed_envelopes_of_type(self, event_type: type[Event] | tuple[type[Event], ...] | None = None) -> List[EventEnvelope]:
        """
        Returns list of all processed EventEnvelopes that match given event type,
        No event type gives full list of processed envelopes.
        """
        return self._envelopes_of_event_type(self._processed, event_type)
    
    def published_envelopes_of_type(self, event_type: type[Event] | tuple[type[Event], ...] | None = None) -> List[EventEnvelope]:
        """
        Returns list of all processed EventEnvelopes that match given event type.
        No event type gives full list of published envelopes.
        """
        return self._envelopes_of_event_type(self._published, event_type)
    
    def unpublished_envelopes_of_type(self, event_type: type[Event] | tuple[type[Event], ...] | None = None) -> List[EventEnvelope]:
        """
        Returns list of all unpublished EventEnvelopes that match given event type.
        No event type gives full list of unpublished envelopes.
        """
        return self._envelopes_of_event_type(self._unpublished, event_type)

    # Event lists
    def processed_events_of_type(self, event_type: type[Event] | tuple[type[Event], ...] | None = None) -> List[Event]:
        """
        Returns list of all processed Events that match given event type.
        No event type gives full list of processed events.
        """
        return self._envelopes_to_events(
            envelopes=self.processed_envelopes_of_type(event_type=event_type)
            )
    
    def published_events_of_type(self, event_type: type[Event] | tuple[type[Event], ...] | None = None) -> List[Event]:
        """
        Returns list of all published Events that match given event type.
        No event type gives full list of published events.
        """
        return self._envelopes_to_events(
            envelopes=self.published_envelopes_of_type(event_type=event_type)
            )
    
    def unpublished_events_of_type(self, event_type: type[Event] | tuple[type[Event], ...] | None = None) -> List[Event]:
        """
        Returns list of all unpublished Events that match given event type.
        No event type gives full list of unpublished events.
        """
        return self._envelopes_to_events(
            envelopes=self.unpublished_envelopes_of_type(event_type=event_type)
            )

    # Event type lists
    def processed_event_types(self, event_type: type[Event] | tuple[type[Event], ...] | None = None) -> List[Type[Event]]:
        """
        Returns list of all processed Event types that match given event type.
        No event type gives full list of processed event types.
        """
        return self._envelopes_to_event_types(
            envelopes=self.processed_envelopes_of_type(event_type=event_type)
            )
    
    # Returns publish order instead of order of execution
    def published_event_types(self, event_type: type[Event] | tuple[type[Event], ...] | None = None) -> List[Type[Event]]:
        """
        Returns list of all published Event types that match given event type.
        No event type gives full list of published event types.
        """
        return self._envelopes_to_event_types(
            envelopes=self.published_envelopes_of_type(event_type=event_type)
            )
    
    def unpublished_event_types(self, event_type: type[Event] | tuple[type[Event], ...] | None = None) -> List[Type[Event]]:
        """
        Returns list of all unpublished Event types that match given event type.
        No event type gives full list of unpublished event types.
        """
        return self._envelopes_to_event_types(
            envelopes=self.unpublished_envelopes_of_type(event_type=event_type)
            )

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