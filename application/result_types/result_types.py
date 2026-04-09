from dataclasses import dataclass
from typing import Union
from domain import Job

class GetNextJobResult:
    pass

@dataclass
class JobAssigned(GetNextJobResult):
    job: Job

@dataclass
class NoJobAvailable(GetNextJobResult):
    pass

NextJobResult = Union[JobAssigned, NoJobAvailable]

class VerifyJob:
    pass

@dataclass
class JobNotFound(VerifyJob):
    pass

@dataclass
class VerificationStarted(VerifyJob):
    pass

VerifyJobResult = Union[JobNotFound, VerificationStarted]
