from abc import ABC, abstractmethod
from typing import Sequence

from application.interfaces.workflow_engine.ProcessStep import ProcessStep

class ProcessDefinition(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable process name."""

    @property
    @abstractmethod
    def steps(self) -> Sequence["ProcessStep"]:
        """Ordered steps that make up the process."""