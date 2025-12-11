from domain import Job
from infrastructure.persistence.models.JobModel import JobModel
from sqlalchemy import func

class JobRepository:
    def __init__(self, session):
        self.session = session


    def get_next_id(self) -> int:
        last_id = self.session.query(func.max(JobModel.id)).scalar()
        return (last_id or 0) + 1
        

    def save(self, job: Job) -> None:
        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)
        return job

    def get_job_by_id(self, job_id: int) -> Job | None:
        return self._store.get(job_id)