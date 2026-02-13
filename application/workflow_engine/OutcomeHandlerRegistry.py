from application.events.EventEnvelope import EventEnvelope
from application.interfaces.workflow_engine.ProcessOutcomeHandler import ProcessOutcomeHandler

class OutcomeHandlerRegistry:
    def __init__(self):
        self._by_event = {}

    def register(self, event_type, handler):
        self._by_event[event_type] = handler

    def get(self, envelope: EventEnvelope) -> ProcessOutcomeHandler:
        event_type = type(envelope.event)
        try:
            handler = self._by_event[event_type]
        except KeyError:
            raise KeyError(f"No OutcomeHandler registered for {event_type}")
        return handler