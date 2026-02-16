from typing import Protocol

from application.events.EventEnvelope import EventEnvelope
from application.workflow_engine.ProcessRunnerResult import ProcessRunnerResult

class ProcessOutcomeHandler(Protocol):
    def on_success(
        self,
        envelope: EventEnvelope,
        result: ProcessRunnerResult,
    ) -> EventEnvelope: ...

    def on_failure(
        self,
        envelope: EventEnvelope,
        result: ProcessRunnerResult,
    ) -> EventEnvelope | None: ...

    def on_retry(
        self,
        envelope: EventEnvelope,
        result: ProcessRunnerResult,
    ) -> EventEnvelope: ...