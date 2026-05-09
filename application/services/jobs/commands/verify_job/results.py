from dataclasses import dataclass
from typing import Union
from uuid import UUID

from domain import Job

class VerifyJob:
    pass

@dataclass
class VerificationStarted(VerifyJob):
    job: Job

@dataclass
class VerifyJobNotFound(VerifyJob):
    job_id: UUID

VerifyJobResult = Union[VerificationStarted, VerifyJobNotFound]