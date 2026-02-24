from application.events.EventEnvelope import EventEnvelope
from application.workflow_engine.ProcessRunnerResult import ProcessRunnerResult
from application.interfaces.workflow_engine.ProcessOutcomeHandler import ProcessOutcomeHandler
from application.events.ApplicationEvents import (
    TranscodeVerified,
    TranscodeVerificationFailed,
    RetryScheduled,
    ApplicationEvent,
)

class JobVerificationOutcomeHandler(ProcessOutcomeHandler):
    def on_success(
        self,
        envelope: EventEnvelope,
        result: ProcessRunnerResult,
    ) -> TranscodeVerified:
        return TranscodeVerified(job_id=envelope.event.job_id,
                                 transcode_file=envelope.event.transcode_file)

    def on_failure(
        self,
        envelope: EventEnvelope,
        result: ProcessRunnerResult,
    ) -> TranscodeVerificationFailed:
        return TranscodeVerificationFailed(job_id=envelope.event.job_id,
                                           transcode_file=envelope.event.transcode_file,
                                           reason=result.failure_info.reason)

    def on_retry(
        self,
        envelope: EventEnvelope,
        result: ProcessRunnerResult,
    ) -> ApplicationEvent:
        return RetryScheduled(original_event=envelope.event)