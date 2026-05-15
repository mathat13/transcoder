from dataclasses import dataclass
from typing import Union

from domain import Job

class CreateJob:
    pass

@dataclass
class JobCreated(CreateJob):
    job: Job

CreateJobResult = Union[JobCreated]