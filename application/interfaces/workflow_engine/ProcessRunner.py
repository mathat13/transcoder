from abc import ABC, abstractmethod

from application.interfaces.workflow_engine.ProcessDefinition import ProcessDefinition
from application.interfaces.workflow_engine.ProcessContext import ProcessContext
from application.interfaces.workflow_engine.ProcessRunnerResult import ProcessRunnerResult

class ProcessRunner(ABC):
    @abstractmethod
    def run(
        self,
        process: ProcessDefinition,
        context: ProcessContext,
    ) -> ProcessRunnerResult:
        ...