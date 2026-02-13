from abc import ABC, abstractmethod

from application.events.EventEnvelope import EventEnvelope
from application.interfaces.workflow_engine.ProcessOutcomeHandler import ProcessOutcomeHandler

class OutcomeHandlerRegistry(ABC):
    @abstractmethod
    def register(self, event_type, handler) -> None:
        pass

    @abstractmethod
    def get(self, envelope: EventEnvelope) -> ProcessOutcomeHandler:
        pass