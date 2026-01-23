from typing import Iterable

from application.events.EventEnvelope import EventEnvelope

from domain import (
    OperationContext,
    Event,
)

class EventPublisher:
    def __init__(self, event_bus):
        self.event_bus = event_bus

    def create_envelope(self, event: Event, operation_context: OperationContext) -> EventEnvelope:
        return EventEnvelope.create(event=event, context=operation_context)

    def publish(self, event: Event, operation_context: OperationContext):
        envelope = self.create_envelope(event=event, operation_context=operation_context)
        self.event_bus.publish(envelope)

    def publish_all(self, events: Iterable[Event], operation_context: OperationContext):
        for event in events:
            self.publish(event=event, operation_context=operation_context)
