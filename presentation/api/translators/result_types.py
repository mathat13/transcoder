from dataclasses import dataclass
from typing import Union

from presentation.api.translators.types import IgnoreReason

from application import CreateJobCommand

@dataclass(frozen=True)
class CommandReady:
    command: CreateJobCommand

@dataclass(frozen=True)
class Ignored:
    reason: IgnoreReason

TranslatorResult = Union[CommandReady, Ignored]