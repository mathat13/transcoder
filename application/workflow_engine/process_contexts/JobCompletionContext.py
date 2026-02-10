from dataclasses import dataclass

from application.workflow_engine.process_contexts.FileContext import FileContext
from application.workflow_engine.process_contexts.MediaContext import MediaContext
from application.workflow_engine.process_contexts.ProcessContext import ProcessContext

@dataclass(frozen=True)
class JobCompletionContext(ProcessContext):
    files: FileContext
    media: MediaContext
