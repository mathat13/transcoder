from dataclasses import dataclass
from typing import Union

from application import CreateJobCommand

@dataclass(frozen=True)
class Admit:
    cmd: CreateJobCommand

TranslatorResult = Union[Admit]