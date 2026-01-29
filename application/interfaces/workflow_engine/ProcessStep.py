from abc import ABC, abstractmethod

from application.interfaces.workflow_engine.ProcessContext import ProcessContext

class ProcessStep(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        """Step name (used for observability)."""

    @abstractmethod
    def execute(self, context: "ProcessContext") -> None:
        """
        Execute the step.

        Raises:
            Exception on failure (expected and mapped upstream).
        """