from uuid import UUID

from application.events.EventEnvelope import EventEnvelope
from application.events.EventPublisher import EventPublisher
from application.interfaces.infrastructure.ports.JobPersistenceCapable import JobPersistenceCapable
from application.events.ApplicationEvents import (TranscodeVerified,
                                                  JobCompletionSuccess,
                                                  JobNotFoundDuringVerification,
                                                  )
from application.result_types.jobservice_result_types import (NextJobResult,
                                                   VerifyJobResult,
                                                   JobAssigned,
                                                   NoJobAvailable,
                                                   VerifyErrorJobNotFound,
                                                   VerificationStarted,
                                                   )


from domain import (
    Job,
    ExternalMediaIDs,
    FileInfo,
    OperationContext,
    JobStatus,
)

class JobService:
    def __init__(self, repo: JobPersistenceCapable, event_publisher: EventPublisher):
        self.repo = repo
        self.event_publisher = event_publisher

    def __call__(self, envelope: EventEnvelope):
        event = envelope.event

        if isinstance(event, TranscodeVerified):
            self._handle_transcode_verified(envelope=envelope)

        if isinstance(event, JobCompletionSuccess):
            self._handle_job_completion_success(envelope=envelope)
        

    def _handle_transcode_verified(self, envelope: EventEnvelope):
        event = envelope.event
        job = self.repo.get_job_by_id(event.job_id)

        if not job:
            self.event_publisher.publish(JobNotFoundDuringVerification(job_id=event.job_id),
                                         operation_context=envelope.context,
                                         )
            return

        self._transition_job(job=job,
                            new_status=JobStatus.success,
                            )
        
        # Persist job and then emit domain events attached to job if successful
        self.repo.save(job)
        self._emit(job, envelope.context)

    def _handle_job_completion_success(self, envelope: EventEnvelope):
        event = envelope.event

        # Idempotent command so don't need to check if job exists
        # At least while we're not archiving jobs
        # Possibly move towards job checking once archiving comes into play
        self.repo.delete(job_id=event.job_id)

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

    def _transition_job(self, job: Job, new_status: JobStatus) -> None:
        job.transition_to(new_status)
    
    def create_job(self, source: str, transcode_output_location: str, media_ids: int) -> Job:
        # Move domain object creation to presentation layer and
        # change job_type and source to ubiquitous language once presentation layer implemented
        operation_context = OperationContext.create()

        media_identities = ExternalMediaIDs.create(media_ids)
        source_file = FileInfo.from_path(source)
        transcode_output = FileInfo.from_path(transcode_output_location)

        job = Job.create(source_file=source_file, transcode_output_file=transcode_output, media_ids=media_identities)

        self.repo.save(job)
        self._emit(job=job, context=operation_context)
        return job
    
    # Future concurrency risk, what if 2 workers try to claim same job?
    def dispatch_job(self) -> NextJobResult:
        operation_context = OperationContext.create()

        job = self.repo.get_next_pending_job()

        if not job:
            return NoJobAvailable()
        
        self._transition_job(job=job,
                             new_status=JobStatus.processing,
                            )
        self.repo.save(job)
        self._emit(job=job, context=operation_context)
        
        return JobAssigned(job=job)

    def verify_job(self, job_id: UUID) -> VerifyJobResult:
        operation_context = OperationContext.create()

        job = self.repo.get_job_by_id(job_id=job_id)

        if not job:
            return VerifyErrorJobNotFound(job_id=job_id)
        
        self._transition_job(job=job,
                             new_status=JobStatus.verifying,
                            )
        
        self.repo.save(job)
        self._emit(job=job, context=operation_context)
        
        return VerificationStarted(job=job)