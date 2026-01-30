from typing import Optional
from dataclasses import dataclass

from application.workflow_engine.FailureInfo import FailureInfo
from application.workflow_engine.ProcessStatus import ProcessStatus
from application.workflow_engine.FailureClassifier import FailureClassifier

@dataclass(frozen=True)
class ProcessRunnerResult():
    status: ProcessStatus
    failure_info: Optional[FailureInfo] = None

    @classmethod
    def success(cls) -> "ProcessRunnerResult":
        return cls(status=ProcessStatus.SUCCESS)

    @classmethod
    def failure(cls,
                exc: Exception,
                classifier: FailureClassifier | None = None,
                ) -> "ProcessRunnerResult":
        classifier = classifier or FailureClassifier()
        return cls(
            status=ProcessStatus.FAILURE,
            failure_info=classifier.classify(exc),
        )