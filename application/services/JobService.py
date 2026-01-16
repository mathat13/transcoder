from uuid import UUID
from copy import deepcopy

from domain import (
    Job,
    ExternalMediaIDs,
    FileInfo,
    OperationContext,
    JobStatus,
)

from application.events.EventEnvelope import EventEnvelope
from application.events.ApplicationEvents import TranscodeVerified

class JobService:
    def __init__(self, repo, event_publisher):
        self.repo = repo
        self.event_publisher = event_publisher

    def __call__(self, envelope: EventEnvelope):
        event = envelope.event

        if type(event) == TranscodeVerified:
            self._handle_transcode_verified(envelope=envelope)

    def _handle_transcode_verified(self, envelope: EventEnvelope):
        event = envelope.event
        job = self.repo._get_job_by_id(event.job_id)

        job = self._transition_job(job=job,
                            new_status=JobStatus.success,
                            )
        
        # Persist job and then emit domain events attached to job
        self.repo.save(job)
        self._emit(job, envelope.context)

    def _emit(self, job: Job, context: OperationContext):
        """
        Takes a job and emits events, job.events has to be deepcopied to allow for clearing of job.events
        before event emission, otherwise event emission becomes untrusted.
        """
        events=deepcopy(job.events)
        job.events.clear()
        self.event_publisher.publish_all(events=events, operation_context=context)

    def _transition_job(self, job: Job, new_status: JobStatus):
        job.transition_to(new_status)
        return job
    
    def create_job(self, source: str, media_ids: int):
        # Move domain object creation to presentation layer and
        # change job_type and source to ubiquitous language once presentation layer implemented
        operation_context = OperationContext.create()

        media_ids = ExternalMediaIDs.create(media_ids)
        source_file = FileInfo.create(source)

        job = Job.create(source_file, media_ids)

        self.repo.save(job)
        self._emit(job=job, context=operation_context)
    
    def dispatch_job(self):
        pass

    def verify_job(self, job_id: UUID):
        operation_context = OperationContext.create()

        job = self.repo._get_job_by_id(job_id=job_id)
        self._transition_job(job=job,
                             new_status=JobStatus.verifying,
                            )
        
        self.repo.save(job)
        self._emit(job=job, context=operation_context)