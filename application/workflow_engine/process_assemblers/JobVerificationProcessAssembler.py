from application.interfaces.workflow_engine.ProcessAssembler import ProcessAssembler
from application.interfaces.infrastructure.ports.FileExistenceCheckCapable import FileExistenceCheckCapable
from application.events.EventEnvelope import EventEnvelope
from application.workflow_engine.process_contexts.JobVerificationContext import JobVerificationContext
from application.workflow_engine.process_contexts.FileContext import FileContext
from application.workflow_engine.ProcessRunnerInput import ProcessRunnerInput
from application.workflow_engine.ProcessDefinition import ProcessDefinition
from application.workflow_engine.process_steps.CheckFileExistence import CheckFileExistence

from domain import (
    JobMovedToVerifying
)

class JobVerificationProcessAssembler(ProcessAssembler):
    event_type = JobMovedToVerifying

    def __init__(self, filesystem: FileExistenceCheckCapable):
        self.fs = filesystem

    def assemble(self, envelope: EventEnvelope) -> ProcessRunnerInput:
        event = envelope.event

        context = JobVerificationContext(
            operation_context=envelope.context,
            envelope=envelope,
            files=FileContext(
                transcode_file=event.transcode_file,
            ),
        )

        process = ProcessDefinition(
            name="job_verification",
            steps=[
                CheckFileExistence(self.fs),
            ],
        )

        return ProcessRunnerInput(
            process_definition=process,
            process_context=context,
        )