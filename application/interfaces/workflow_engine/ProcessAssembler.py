from abc import ABC, abstractmethod

from application.events.EventEnvelope import EventEnvelope

class ProcessAssembler(ABC):
    @abstractmethod
    def assemble(self, envelope: EventEnvelope):
        ...