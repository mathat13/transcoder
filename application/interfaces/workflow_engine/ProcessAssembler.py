from abc import ABC, abstractmethod

from application.events.EventEnvelope import EventEnvelope

class ProcessAssembler(ABC):
    @abstractmethod
    def create(self, envelope: EventEnvelope):
        ...