from dataclasses import dataclass
from typing import Union
from uuid import UUID

from domain import Job

class CreateJobResult:
    pass

@dataclass
class JobCreationSuccess(CreateJobResult):
    job_id: UUID


class DispatchJob:
    pass

@dataclass
class JobAssigned(DispatchJob):
    job: Job

@dataclass
class DispatchErrorNoJobAvailable(DispatchJob):
    pass

DispatchJobResult = Union[JobAssigned, DispatchErrorNoJobAvailable]

class VerifyJob:
    pass

@dataclass
class VerifyErrorJobNotFound(VerifyJob):
    job_id: UUID

@dataclass
class VerificationStarted(VerifyJob):
    job: Job

VerifyJobResult = Union[VerifyErrorJobNotFound, VerificationStarted]
