from dataclasses import dataclass

@dataclass
class DomainEvent:
    pass

@dataclass
class JobStatusChanged(DomainEvent):
    job_id: int
    old_status: str
    new_status: str

@dataclass
class JobCreated(DomainEvent):
    job_id: int
    job_status: str
    source_path: str