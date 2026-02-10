from application.workflow_engine.process_contexts.ProcessContext import ProcessContext
from application.interfaces.workflow_engine.ProcessStep import ProcessStep
from application.interfaces.infrastructure.ports.FileDeletionCapable import FileDeletionCapable

class DeleteSourceFile(ProcessStep):
    fs: FileDeletionCapable

    def __init__(self, filesystem):
        self.fs = filesystem

    @property
    def name(self) -> str:
        """Step name (used for observability)."""
        return "Delete original file"

    def execute(self, context: "ProcessContext") -> None:
        """
        Execute the step.

        Raises:
            Exception on failure (expected and mapped upstream).
        """
        self.fs.delete(context.files.source_file.path)