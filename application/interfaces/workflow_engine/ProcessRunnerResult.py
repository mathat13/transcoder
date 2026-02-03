from abc import ABC, abstractmethod
from  typing import Optional

from application.workflow_engine.FailureInfo import FailureInfo
from application.workflow_engine.ProcessStatus import ProcessStatus
from application.interfaces.workflow_engine.FailureClassifier import FailureClassifier

class ProcessRunnerResult(ABC):
    status: ProcessStatus
    failure: Optional[FailureInfo] = None

    @classmethod
    @abstractmethod
    def success(self) -> "ProcessRunnerResult":
        ...

    @classmethod
    @abstractmethod
    def failure(self, exc: Exception, classifier: FailureClassifier | None = None,) -> "ProcessRunnerResult":
        ...