from dataclasses import dataclass
from typing import Union

from domain import Job

@dataclass
class JobFound:
    job: Job

@dataclass
class JobNotFound:
    pass

GetJobByIDResult = Union[JobFound, JobNotFound]