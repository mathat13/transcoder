from abc import ABC, abstractmethod

from application.events.EventEnvelope import EventEnvelope
from application.workflow_engine.ProcessRunnerInput import ProcessRunnerInput

class ProcessAssembler(ABC):
    @abstractmethod
    def assemble(self, envelope: EventEnvelope) -> ProcessRunnerInput:
        ...