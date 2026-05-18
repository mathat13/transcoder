from dataclasses import dataclass
from typing import Union
from typing import Literal

from application import CreateJobCommand

IngressNonSuccessReason = Literal[
    "unsupported_event_type",
    ]

@dataclass(frozen=True)
class Admit:
    cmd: CreateJobCommand

@dataclass(frozen=True)
class Deny:
    reason: IngressNonSuccessReason

TranslatorResult = Union[Admit, Deny]