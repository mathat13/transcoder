from abc import ABC, abstractmethod
from typing import Optional

from application.interfaces.workflow_engine.FailureReason import FailureReason

class ProcessRunnerResult(ABC):
    @property
    @abstractmethod
    def success(self) -> bool:
        ...

    @property
    @abstractmethod
    def failure_reason(self) -> Optional["FailureReason"]:
        ...

    @property
    @abstractmethod
    def failed_step(self) -> Optional[str]:
        ...

    @property
    @abstractmethod
    def exception(self) -> Optional[Exception]:
        ...