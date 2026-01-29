from abc import ABC, abstractmethod

from application.events.EventEnvelope import EventEnvelope

class ProcessManager(ABC):
    @abstractmethod
    def handle(self, envelope: "EventEnvelope") -> None:
        """
        Entry point from event bus.
        Decides whether to run, retry, or abandon a process.
        """