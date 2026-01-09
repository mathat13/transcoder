from uuid import UUID

from domain import (
    Job,
    ExternalMediaIDs,
    FileInfo,
)

class JobService:
    def __init__(self, repo, event_bus):
        self.repo = repo
        self.event_bus = event_bus
    
    def create_job(self, source: str, media_ids: int):
        # Move to presentation layer and change job_type and source to ubiquitous language
        # Once presentation layer implemented
        media_ids = ExternalMediaIDs.create(media_ids)
        source_file = FileInfo.create(source)

        job = Job.create(source_file, media_ids)

        self.repo.save(job)

        # Dispatch domain events
        self.event_bus.publish_all(job.events)
        job.events.clear()

        return job

    def transition_job(self, job_id: UUID, new_status: str):
        job = self.repo._get_job_by_id(job_id)
        job.transition_to(new_status)

        self.repo.save(job)

        # Dispatch domain events
        self.event_bus.publish_all(job.events)
        job.events.clear()

        return job