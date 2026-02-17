from typing import (
    Dict,
    Type,
)

from application.events.EventEnvelope import EventEnvelope
from application.interfaces.workflow_engine.ProcessOutcomeHandler import ProcessOutcomeHandler

from domain import (
    Event,
)

class OutcomeHandlerRegistry:
    # Missing keys raise KeyError
    _by_event: Dict[Type[Event], ProcessOutcomeHandler]

    def __init__(self):
        self._by_event = {}

    def register(self, event_type: Type[Event], handler: ProcessOutcomeHandler):
        self._by_event[event_type] = handler

    def get(self, envelope: EventEnvelope) -> ProcessOutcomeHandler:
        event_type = type(envelope.event)
        try:
            handler = self._by_event[event_type]
        except KeyError:
            raise KeyError(f"No OutcomeHandler registered for {event_type}")
        return handler