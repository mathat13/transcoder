from application.events.EventEnvelope import EventEnvelope
from application.workflow_engine.ProcessRunnerResult import ProcessRunnerResult

class JobCompletionOutcomeHandler:
    def on_success(
        self,
        envelope: EventEnvelope,
        result: ProcessRunnerResult,
    ) -> EventEnvelope:
        pass

    def on_failure(
        self,
        envelope: EventEnvelope,
        result: ProcessRunnerResult,
    ) -> EventEnvelope | None:
        pass

    def on_retry(
        self,
        envelope: EventEnvelope,
        result: ProcessRunnerResult,
    ) -> EventEnvelope:
        pass