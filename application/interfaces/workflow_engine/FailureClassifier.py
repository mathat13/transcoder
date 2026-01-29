from abc import ABC, abstractmethod

from application.workflow_engine.FailureInfo import FailureInfo

class FailureClassifier(ABC):
    @abstractmethod
    def classify(self, exc: Exception) -> "FailureInfo":
        ...