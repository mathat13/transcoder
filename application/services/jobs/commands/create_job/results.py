from dataclasses import dataclass
from typing import Union

from domain import Job

class CreateJob:
    pass

@dataclass
class JobCreatedResult(CreateJob):
    job: Job

CreateJobResult = Union[JobCreatedResult]