from dataclasses import dataclass

from application.workflow_engine.process_contexts.FileContext import FileContext
from application.workflow_engine.process_contexts.ProcessContext import ProcessContext

@dataclass(frozen=True)
class JobVerificationContext(ProcessContext):
    files: FileContext