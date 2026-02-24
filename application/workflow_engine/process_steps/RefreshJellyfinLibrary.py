from application.workflow_engine.process_contexts.ProcessContext import ProcessContext
from application.interfaces.workflow_engine.ProcessStep import ProcessStep
from application.interfaces.infrastructure.ports.JellyfinLibraryRefreshCapable import JellyfinLibraryRefreshCapable

class RefreshJellyfinLibrary(ProcessStep):
    jellyfin: JellyfinLibraryRefreshCapable

    def __init__(self, jellyfin: JellyfinLibraryRefreshCapable):
        self.jellyfin = jellyfin

    @property
    def name(self) -> str:
        """Step name (used for observability)."""
        return "Refresh Jellyfin library"

    def execute(self, process_context: "ProcessContext") -> None:
        """
        Execute the step.

        Raises:
            Exception on failure (expected and mapped upstream).
        """
        self.jellyfin.refresh_library(context=process_context.operation_context)