from abc import ABC, abstractmethod

from application.workflow_engine.ProcessDefinition import ProcessDefinition
from application.workflow_engine.process_contexts.ProcessContext import ProcessContext
from application.interfaces.workflow_engine.ProcessRunnerResult import ProcessRunnerResult

class ProcessRunner(ABC):
    @abstractmethod
    def run(
        self,
        process: ProcessDefinition,
        context: ProcessContext,
    ) -> ProcessRunnerResult:
        ...