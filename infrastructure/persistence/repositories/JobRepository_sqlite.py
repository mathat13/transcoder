from domain import Job
from infrastructure.persistence.models.JobModel import JobModel
from infrastructure.persistence.models.mappers.JobMapper import JobMapper

from sqlalchemy import func

class JobRepository:
    def __init__(self, session):
        self.session = session

    def save(self, job: Job) -> None:
        job_record = JobMapper.to_JobModel(job)
        self.session.add(job_record)
        self.session.commit()
        self.session.refresh(job_record)

    def get_job_by_id(self, job_id: int) -> Job | None:
        retrieved_job_record = self.session.query(JobModel).filter(JobModel.id == job_id).first()
        return JobMapper.to_Job(retrieved_job_record)