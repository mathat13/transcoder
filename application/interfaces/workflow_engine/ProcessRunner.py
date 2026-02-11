from abc import ABC, abstractmethod

from application.workflow_engine.ProcessRunnerInput import ProcessRunnerInput
from application.interfaces.workflow_engine.ProcessRunnerResult import ProcessRunnerResult

class ProcessRunner(ABC):
    @abstractmethod
    def run(
        self,
        payload: ProcessRunnerInput,
    ) -> ProcessRunnerResult:
        pass