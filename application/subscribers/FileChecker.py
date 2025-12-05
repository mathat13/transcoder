from domain import JobCreated, JobTranscodeCompleted

class FileChecker:
    def __init__(self, filesystem, logger):
        self.fs = filesystem      # injected dependency
        self.logger = logger

    def __call__(self, event):
        """Single entrypoint — dispatch internally."""
        
        if isinstance(event, JobCreated):
            return self._handle_job_created(event)

        if isinstance(event, JobTranscodeCompleted):
            return self._handle_transcode_completed(event)

        # Fallback if something weird happens
        raise TypeError(f"Unhandled event type {type(event)}")

    # --- internal handlers ---

    def _handle_job_created(self, event: JobCreated):
        if not self.fs.exists(event.source_path):
            self.logger.publish_error(f"[Job {event.job_id}] Source missing: {event.source_path}")
            #optionally: publish another event OR mark job invalid
        else:
            self.logger.publish_message(f"[Job {event.job_id}] Source OK")

    def _handle_transcode_completed(self, event: JobTranscodeCompleted):
        if not self.fs.exists(event.output_path):
            self.logger.publish_error(f"[Job {event.job_id}] Output missing: {event.output_path}")
        else:
            self.logger.publish_message(f"[Job {event.job_id}] Output OK")
