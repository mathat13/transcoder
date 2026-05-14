from dataclasses import dataclass
from typing import Union

from domain import Job

class DispatchJob:
    pass

@dataclass
class JobDispatched(DispatchJob):
    job: Job

@dataclass
class NoJobAvailable(DispatchJob):
    pass

DispatchJobResult = Union[JobDispatched, NoJobAvailable]