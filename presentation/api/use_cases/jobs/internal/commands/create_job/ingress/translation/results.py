from dataclasses import dataclass
from typing import Union

from application import CreateJobCommand

@dataclass(frozen=True)
class CommandReady:
    cmd: CreateJobCommand

TranslatorResult = Union[CommandReady]