from domain import JobStatusChanged, JobStatus
from application.events.ApplicationEvents import TranscodeVerified, TranscodeVerificationFailed

class JobVerifyingOrchestrator:
    def __init__(self, event_bus, logger, file_checker):
        self.bus = event_bus
        self.logger = logger
        self.file_checker = file_checker

    def __call__(self, event: JobStatusChanged):
        if event.new_status == JobStatus.verifying:
            self._VerifyTranscodeCompleted(event)
        # Add further workflows as needed
        
    def _VerifyTranscodeCompleted(self, event):
        if not self.file_checker.exists(event.output_path):
            self.logger.publish_error(f"[Job {event.job_id}] Output missing: {event.output_path}")
            self.bus.publish(TranscodeVerificationFailed(job_id=event.job_id,file_path=event.output_path))
            return
        
        self.logger.publish_message(f"[Job {event.job_id}] Output OK")
        self.bus.publish(TranscodeVerified(job_id=event.job_id,file_path=event.output_path))