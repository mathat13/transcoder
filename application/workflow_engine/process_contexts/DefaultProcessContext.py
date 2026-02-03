from dataclasses import dataclass

from application.workflow_engine.process_contexts.ProcessContext import ProcessContext

@dataclass(frozen=True)
class DefaultProcessContext(ProcessContext):
      pass