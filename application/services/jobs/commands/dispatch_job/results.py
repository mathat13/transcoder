from dataclasses import dataclass
from typing import Union

from domain import Job

class DispatchJob:
    pass

@dataclass
class JobDispatched(DispatchJob):
    job: Job

@dataclass
class DispatchJobNoJobAvailable(DispatchJob):
    pass

DispatchJobResult = Union[JobDispatched, DispatchJobNoJobAvailable]