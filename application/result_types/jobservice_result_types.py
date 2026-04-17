from dataclasses import dataclass
from typing import Union
from uuid import UUID

from domain import Job

class CreateJobResult:
    pass

@dataclass
class JobCreationSuccess(CreateJobResult):
    job_id: UUID


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
class VerifyErrorJobNotFound(VerifyJob):
    job_id: UUID

@dataclass
class VerificationStarted(VerifyJob):
    job: Job

VerifyJobResult = Union[VerifyErrorJobNotFound, VerificationStarted]
