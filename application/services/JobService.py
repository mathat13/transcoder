from uuid import UUID

from domain import (
    Job,
    ExternalMediaIDs,
    FileInfo,
    OperationContext,
    JobStatus,
)

from application.events.EventEnvelope import EventEnvelope
from application.events.EventPublisher import EventPublisher
from application.interfaces.infrastructure.ports.JobPersistenceCapable import JobPersistenceCapable
from application.events.ApplicationEvents import TranscodeVerified

class JobService:
    def __init__(self, repo: JobPersistenceCapable, event_publisher: EventPublisher):
        self.repo = repo
        self.event_publisher = event_publisher

    def __call__(self, envelope: EventEnvelope):
        event = envelope.event

        if isinstance(event, TranscodeVerified):
            self._handle_transcode_verified(envelope=envelope)

    def _handle_transcode_verified(self, envelope: EventEnvelope):
        event = envelope.event
        job = self.repo.get_job_by_id(event.job_id)

        job = self._transition_job(job=job,
                            new_status=JobStatus.success,
                            )
        
        # Persist job and then emit domain events attached to job if successful
        self.repo.save(job)
        self._emit(job, envelope.context)

    # Placholder while event outbox is not implemented
    # Not the nicest as it modifies an object that isn't itself, use with caution
    # Decided to take a Job object as a parameter to be as explicit as possible
    def _emit(self, job: Job, context: OperationContext) -> None:
        """
        Takes a job and emits events, job.events has to be deepcopied to allow for clearing of job.events
        before event emission, otherwise event emission becomes untrusted.
        """
        events=job.pull_events()
        self.event_publisher.publish_all(events=events, operation_context=context)

    def _transition_job(self, job: Job, new_status: JobStatus) -> Job:
        job.transition_to(new_status)
        return job
    
    def create_job(self, source: str, media_ids: int) -> None:
        # Move domain object creation to presentation layer and
        # change job_type and source to ubiquitous language once presentation layer implemented
        operation_context = OperationContext.create()

        media_identities = ExternalMediaIDs.create(media_ids)
        source_file = FileInfo.create(source)

        job = Job.create(source_file, media_identities)

        self.repo.save(job)
        self._emit(job=job, context=operation_context)
    
    def dispatch_job(self):
        pass

    def verify_job(self, job_id: UUID) -> None:
        operation_context = OperationContext.create()

        job = self.repo.get_job_by_id(job_id=job_id)
        self._transition_job(job=job,
                             new_status=JobStatus.verifying,
                            )
        
        self.repo.save(job)
        self._emit(job=job, context=operation_context)