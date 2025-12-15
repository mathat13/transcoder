from domain import Job

class FakeJobRepository:
    def __init__(self):
        self._store = {}

    def save(self, job: Job) -> None:
        self._store[job.id] = job

    def get(self, job_id: int) -> Job | None:
        return self._store.get(job_id)
