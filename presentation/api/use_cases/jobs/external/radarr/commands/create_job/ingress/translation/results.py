from dataclasses import dataclass
from typing import Union

from presentation.api.use_cases.jobs.external.radarr.commands.create_job.ingress.translation.types import IgnoreReason

from application import CreateJobCommand

@dataclass(frozen=True)
class CommandReady:
    cmd: CreateJobCommand

@dataclass(frozen=True)
class Ignored:
    reason: IgnoreReason

TranslatorResult = Union[CommandReady, Ignored]