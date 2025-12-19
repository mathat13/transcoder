from uuid import UUID

from domain import Job

class JobService:
    def __init__(self, repo, event_bus):
        self.repo = repo
        self.event_bus = event_bus
    
    def create_job(self, job_type: str, source: str):
        job = Job.create(job_type, source)

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