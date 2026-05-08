from dataclasses import dataclass
from typing import Union
from uuid import UUID

from domain import Job

class VerifyJob:
    pass

@dataclass
class VerifyErrorJobNotFound(VerifyJob):
    job_id: UUID

@dataclass
class VerificationStarted(VerifyJob):
    job: Job

VerifyJobResult = Union[VerifyErrorJobNotFound, VerificationStarted]