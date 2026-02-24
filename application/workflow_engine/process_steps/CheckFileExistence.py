from application.workflow_engine.process_contexts.ProcessContext import ProcessContext
from application.interfaces.workflow_engine.ProcessStep import ProcessStep
from application.interfaces.infrastructure.ports.FileExistenceCheckCapable import FileExistenceCheckCapable

class CheckFileExistence(ProcessStep):
    fs: FileExistenceCheckCapable

    def __init__(self, filesystem: FileExistenceCheckCapable):
        self.fs = filesystem

    @property
    def name(self) -> str:
        """Step name (used for observability)."""
        return "Check a file exists"

    def execute(self, process_context: "ProcessContext") -> None:
        """
        Execute the step.

        Raises:
            Exception on failure (expected and mapped upstream).
        """
        self.fs.assert_file_existence(file=process_context.files.source_file.path)