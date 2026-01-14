from uuid import UUID

from domain import (
    Job,
    ExternalMediaIDs,
    FileInfo,
    OperationContext,
)

from application.events.EventPublisher import EventPublisher

class JobService:
    def __init__(self, repo, event_publisher):
        self.repo = repo
        self.event_publisher = event_publisher
    
    def create_job(self, source: str, media_ids: int):
        # Move to presentation layer and change job_type and source to ubiquitous language
        # Once presentation layer implemented
        operation_context = OperationContext.create()

        media_ids = ExternalMediaIDs.create(media_ids)
        source_file = FileInfo.create(source)

        job = Job.create(source_file, media_ids)

        self.repo.save(job)

        # Dispatch domain events
        self.event_publisher.publish_all(job.events, operation_context)
        job.events.clear()

        return job

    def transition_job(self, job_id: UUID, new_status: str):
        operation_context = OperationContext.create()

        job = self.repo._get_job_by_id(job_id)
        job.transition_to(new_status)

        self.repo.save(job)

        # Dispatch domain events
        self.event_publisher.publish_all(job.events, operation_context)
        job.events.clear()

        return job