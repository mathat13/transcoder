import pytest
from typing import Sequence

from tests.bootstrap.bootstrap_test_system import bootstrap_workflow_test_system
from tests.factories.EventFactories import (EventEnvelopeFactory,
                                            JobMovedToVerifyingEventFactory,
                                            JobCompletedEventFactory,
                                            )

from domain import (
    JobStatus,
)
from application import (
    ProcessStep,
    DefaultProcessRunner,
    ProcessRunnerInput,
    ProcessContext,
    ProcessDefinition,
    ProcessStatus,
)

class RecordingStep(ProcessStep):
    def __init__(self):
        self.executed = False
    
    @property
    def name(self) -> str:
        return "Recording test step."

    def execute(self, process_context: ProcessContext):
        self.executed = True

class FailingStep(ProcessStep):
    def __init__(self):
        self.executed = False
    
    @property
    def name(self) -> str:
        return "Failing test step."

    def execute(self, process_context: ProcessContext):
        self.executed = True
        raise RuntimeError("boom")
    
def test_runner_stops_on_failure():
    runner = DefaultProcessRunner()
    step1 = RecordingStep()
    step2 = FailingStep()
    step3 = RecordingStep()

    def make_payload(process_steps: Sequence[ProcessStep]) -> ProcessRunnerInput:
        return ProcessRunnerInput(
            ProcessDefinition("test", process_steps),
            ProcessContext(None, None)
            )

    payload = make_payload([step1, step2, step3])

    result = runner.run(payload)

    assert step1.executed
    assert step2.executed
    assert not step3.executed
    assert result.status is ProcessStatus.FAILURE

def test_runner_success():
    runner = DefaultProcessRunner()

    steps = [
        RecordingStep(),
        RecordingStep(),
    ]

    def make_payload(process_steps: Sequence[ProcessStep]) -> ProcessRunnerInput:
        return ProcessRunnerInput(
            ProcessDefinition("test", process_steps),
            ProcessContext(None, None)
            )

    payload = make_payload(steps)

    result = runner.run(payload)

    assert result.status is ProcessStatus.SUCCESS
    assert all(step.executed for step in steps)

def test_runner_verification_flow():
    
    # Setup
    system = bootstrap_workflow_test_system(runner=DefaultProcessRunner())
    envelope = EventEnvelopeFactory(event=JobMovedToVerifyingEventFactory())
    system.filesystem.add(envelope.event.transcode_output_file.path)
    payload = system.assembler_registry.assemble(envelope=envelope)

    # Execute
    result = system.runner.run(payload=payload)

    assert result.status == ProcessStatus.SUCCESS

def test_runner_completion_flow():
    
    # Setup
    system = bootstrap_workflow_test_system(runner=DefaultProcessRunner())
    envelope = EventEnvelopeFactory(event=JobCompletedEventFactory())
    system.filesystem.add(envelope.event.source_file.path)
    system.filesystem.add(envelope.event.transcode_output_file.path)
    system.radarr.add_movie(media_identifiers=envelope.event.media_ids,
                            file=envelope.event.source_file,
                            context=envelope.context)
    payload = system.assembler_registry.assemble(envelope=envelope)

    # Execute
    result = system.runner.run(payload=payload)

    assert result.status == ProcessStatus.SUCCESS