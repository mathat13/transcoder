from dataclasses import dataclass
from typing import Union

from domain import Job

@dataclass
class GetJobByIDFound:
    job: Job

@dataclass
class GetJobByIDNotFound:
    pass

GetJobByIDResult = Union[GetJobByIDFound, GetJobByIDNotFound]