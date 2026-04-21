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
class JobDispatched(DispatchJob):
    job: Job

@dataclass
class DispatchJobNoJobAvailable(DispatchJob):
    pass

DispatchJobResult = Union[JobDispatched, DispatchJobNoJobAvailable]

class VerifyJob:
    pass

@dataclass
class VerifyErrorJobNotFound(VerifyJob):
    job_id: UUID

@dataclass
class VerificationStarted(VerifyJob):
    job: Job

VerifyJobResult = Union[VerifyErrorJobNotFound, VerificationStarted]
