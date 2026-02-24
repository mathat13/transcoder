import pytest
from typing import Sequence

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