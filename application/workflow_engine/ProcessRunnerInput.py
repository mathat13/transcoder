from dataclasses import dataclass

from application.workflow_engine.process_contexts.ProcessContext import ProcessContext
from application.workflow_engine.ProcessDefinition import ProcessDefinition

@dataclass(frozen=True)
class ProcessRunnerInput:
    process_definition: ProcessDefinition
    process_context: ProcessContext