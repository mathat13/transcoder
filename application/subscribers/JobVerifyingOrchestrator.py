from domain import JobMovedToVerifying, JobStatus
from application.events.ApplicationEvents import TranscodeVerified, TranscodeVerificationFailed

class JobVerifyingOrchestrator:
    def __init__(self, event_bus, logger, filesystem):
        self.bus = event_bus
        self.logger = logger
        self.filesystem = filesystem

    def __call__(self, event: JobMovedToVerifying):
        self._VerifyTranscodeCompleted(event)
        # Add further workflows as needed
        
    def _VerifyTranscodeCompleted(self, event):
        if not self.filesystem.exists(event.transcode_file):
            self.logger.publish_error(f"[Job {event.job_id}] Output missing: {event.transcode_file}")
            self.bus.publish(TranscodeVerificationFailed(job_id=event.job_id,transcode_file=event.transcode_file))
            return
        
        self.logger.publish_message(f"[Job {event.job_id}] Output OK")
        self.bus.publish(TranscodeVerified(job_id=event.job_id,transcode_file=event.transcode_file))