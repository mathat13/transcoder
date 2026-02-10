from application.workflow_engine.process_contexts.ProcessContext import ProcessContext
from application.interfaces.workflow_engine.ProcessStep import ProcessStep

from application.interfaces.infrastructure.ports.HardlinkCapable import HardlinkCapable

class HardlinkFile(ProcessStep):
    fs: HardlinkCapable
    
    def __init__(self, filesystem):
        self.fs = filesystem

    @property
    def name(self) -> str:
        """Step name (used for observability)."""
        return "Hardlink source file to watch directory"

    def execute(self, context: "ProcessContext") -> None:
        """
        Execute the step.

        Raises:
            Exception on failure (expected and mapped upstream).
        """
        self.fs.hardlink(context.files.source_file.path, context.files.transcode_file.path)
