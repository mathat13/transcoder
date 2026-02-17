from application.interfaces.workflow_engine.ProcessAssembler import ProcessAssembler
from application.events.EventEnvelope import EventEnvelope
from application.workflow_engine.process_contexts.JobCompletionContext import JobCompletionContext
from application.workflow_engine.process_contexts.FileContext import FileContext
from application.workflow_engine.process_contexts.MediaContext import MediaContext
from application.workflow_engine.ProcessRunnerInput import ProcessRunnerInput
from application.workflow_engine.ProcessDefinition import ProcessDefinition
from application.workflow_engine.process_steps.UpdateRadarrMovieFile import UpdateRadarrMovieFile
from application.workflow_engine.process_steps.DeleteSourceFile import DeleteSourceFile
from application.workflow_engine.process_steps.HardlinkFile import HardlinkFile
from application.workflow_engine.process_steps.RefreshJellyfinLibrary import RefreshJellyfinLibrary

from domain import (
    JobCompleted
)

class JobCompletionProcessAssembler(ProcessAssembler):
    event_type = JobCompleted

    def __init__(self, filesystem, radarr, jellyfin):
        self.fs = filesystem
        self.radarr = radarr
        self.jellyfin = jellyfin

    def assemble(self, envelope: EventEnvelope) -> ProcessRunnerInput:
        event = envelope.event

        context = JobCompletionContext(
            operation_context=envelope.context,
            envelope=envelope,
            files=FileContext(
                source_file=event.source_file,
                transcode_file=event.transcode_file,
            ),
            media=MediaContext(
                media_ids=event.media_ids
            ),
        )

        process = ProcessDefinition(
            name="job_completion",
            steps=[
                HardlinkFile(filesystem=self.fs),
                UpdateRadarrMovieFile(radarr=self.radarr),
                DeleteSourceFile(filesystem=self.fs),
                RefreshJellyfinLibrary(jellyfin=self.jellyfin),
            ],
        )

        return ProcessRunnerInput(
            process_definition=process,
            process_context=context,
        )