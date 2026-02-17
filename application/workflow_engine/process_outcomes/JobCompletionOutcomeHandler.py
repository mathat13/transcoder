from application.events.EventEnvelope import EventEnvelope
from application.workflow_engine.ProcessRunnerResult import ProcessRunnerResult
from application.interfaces.workflow_engine.ProcessOutcomeHandler import ProcessOutcomeHandler
from application.events.ApplicationEvents import (
    JobCompletionFailure,
    JobCompletionSuccess,
    RetryScheduled,
    ApplicationEvent,
)

class JobCompletionOutcomeHandler(ProcessOutcomeHandler):
    def on_success(
        self,
        envelope: EventEnvelope,
        result: ProcessRunnerResult,
    ) -> JobCompletionSuccess:
        return JobCompletionSuccess(job_id=envelope.event.job_id)

    def on_failure(
        self,
        envelope: EventEnvelope,
        result: ProcessRunnerResult,
    ) -> JobCompletionFailure:
        return JobCompletionFailure(job_id=envelope.event.job_id,
                                    reason=result.failure_info.reason)

    def on_retry(
        self,
        envelope: EventEnvelope,
        result: ProcessRunnerResult,
    ) -> ApplicationEvent:
        return RetryScheduled(original_event=envelope.event)