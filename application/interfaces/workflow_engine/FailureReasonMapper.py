from abc import ABC, abstractmethod

from application.interfaces.workflow_engine.FailureReason import FailureReason

class FailureReasonMapper(ABC):
    @abstractmethod
    def map(self, exc: Exception) -> FailureReason:
        """Convert exception into a failure reason."""