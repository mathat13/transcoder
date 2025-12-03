from domain import Job

class FakeJobRepository:
    def __init__(self):
        self._store = {}
        self._next_id = 1

    def next_id(self) -> int:
        nid = self._next_id
        self._next_id += 1
        return nid

    def save(self, job: Job) -> None:
        self._store[job.id] = job

    def get(self, job_id: int) -> Job | None:
        return self._store.get(job_id)
