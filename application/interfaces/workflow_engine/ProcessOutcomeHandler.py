from abc import ABC, abstractmethod

from application.events.EventEnvelope import EventEnvelope
from application.workflow_engine.ProcessRunnerResult import ProcessRunnerResult

class ProcessOutcomeHandler(ABC):
    @abstractmethod
    def on_success(
        self,
        envelope: EventEnvelope,
        result: ProcessRunnerResult,
    ) -> EventEnvelope: ...

    @abstractmethod
    def on_failure(
        self,
        envelope: EventEnvelope,
        result: ProcessRunnerResult,
    ) -> EventEnvelope | None: ...

    @abstractmethod
    def on_retry(
        self,
        envelope: EventEnvelope,
        result: ProcessRunnerResult,
    ) -> EventEnvelope: ...