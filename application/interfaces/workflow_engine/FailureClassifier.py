from abc import ABC, abstractmethod

from application.interfaces.workflow_engine.FailureInfo import FailureInfo

class FailureClassifier(ABC):
    @abstractmethod
    def classify(self, exc: Exception) -> "FailureInfo":
        ...