from typing import Sequence
from dataclasses import dataclass

from application.interfaces.workflow_engine.ProcessStep import ProcessStep

@dataclass(frozen=True)
class ProcessDefinition:
    name: str
    steps: Sequence["ProcessStep"]