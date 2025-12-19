from uuid import UUID

from domain import Job
from infrastructure.persistence.models.JobModel import JobModel
from infrastructure.persistence.models.mappers.JobMapper import JobMapper

class JobRepository:
    def __init__(self, session):
        self.session = session

    def _get_job_by_id(self, job_id: UUID) -> Job | None:
        retrieved_job_record = (
            self.session.query(JobModel)
            .filter(JobModel.id == str(job_id))
            .first()
        )

        if retrieved_job_record is None:
            return None
        
        return JobMapper.to_Job(retrieved_job_record)
    
    def save(self, job: Job) -> None:

        job_record = JobMapper.to_JobModel(job)
        self.session.add(job_record)
        self.session.commit()
        self.session.refresh(job_record)

    def get_next_pending_job(self) -> Job | None:
        next_job_model = (
            self.session.query(JobModel)
            .filter(JobModel.status == "pending")
            .order_by(JobModel.created_at.asc())
            .first()
        )
        if next_job_model is None:
            return None
        
        return JobMapper.to_Job(next_job_model)
