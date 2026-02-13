import pytest

from application import (
    FailureClassifier,
    FailureInfo,
    ProcessRunnerResult,
    ProcessStatus,
    FailureReason,
    SourceFileMissing,
    FileSystemIOError,
    APIServiceException,
    ProcessStep,
    ProcessRunner,
    ProcessRunnerInput,
    ProcessContext,
    ProcessDefinition,
)

from tests import (
    JobCompletedEventFactory,
)

@pytest.mark.parametrize(
    "exception, expected_reason",
    [
        (SourceFileMissing("/file.mp4"), FailureReason.FILESYSTEM_LOGIC),
        (FileSystemIOError("hardlink", "/file.mp4", OSError), FailureReason.FILESYSTEM_IO),
        (APIServiceException("Radarr", 500, True, None), FailureReason.API_CALL_FAILURE),
        (APIServiceException("Radarr", 404, False, None), FailureReason.API_CALL_FAILURE),
        (OverflowError(), FailureReason.UNKNOWN),
    ],
)

def test_FailureClassifier_classifies_exceptions_correctly(exception, expected_reason):
    classifier = FailureClassifier()

    # Ensure retryable exists for UNKNOWN case (only required for tests.)
    if not hasattr(exception, "retryable"):
        exception.retryable = False
        
    failure_info = classifier.classify(exception)

    assert failure_info.reason == expected_reason
    assert failure_info.retryable == exception.retryable
    assert failure_info.detail == str(exception)

def test_ProcessRunnerResult_generates_correct_success_response():
    success_response = ProcessRunnerResult.success()

    assert isinstance(success_response, ProcessRunnerResult)
    assert success_response.status == ProcessStatus.SUCCESS
    assert success_response.failure_info == None

@pytest.mark.parametrize(
    "exception, expected_reason",
    [
        (SourceFileMissing("/file.mp4"), FailureReason.FILESYSTEM_LOGIC),
        (FileSystemIOError("hardlink", "/file.mp4", OSError), FailureReason.FILESYSTEM_IO),
        (APIServiceException("Radarr", 500, True, None), FailureReason.API_CALL_FAILURE),
        (APIServiceException("Radarr", 404, False, None), FailureReason.API_CALL_FAILURE),
        (OverflowError(), FailureReason.UNKNOWN),
    ],
)

def test_ProcessRunnerResult_generates_correct_failure_response(exception, expected_reason):

    # Ensure retryable exists for UNKNOWN case (only required for tests.)
    if not hasattr(exception, "retryable"):
        exception.retryable = False

    classifier = FailureClassifier()

    failure_response_without_classifier_param = ProcessRunnerResult.failure(exc=exception)
    failure_response_with_classifier_param = ProcessRunnerResult.failure(exc=exception, classifier=classifier)

    for failure_response in [failure_response_without_classifier_param, failure_response_with_classifier_param]:
        assert isinstance(failure_response, ProcessRunnerResult)
        assert failure_response.status == ProcessStatus.FAILURE

        # failure_info
        failure = failure_response.failure_info
        assert failure is not None
        assert isinstance(failure, FailureInfo)
        assert failure.reason == expected_reason
        assert failure.retryable == exception.retryable
        assert failure.detail == str(exception)

class RecordingStep(ProcessStep):
    def __init__(self):
        self.executed = False
    
    @property
    def name(self) -> str:
        return "Recording test step."

    def execute(self, context):
        self.executed = True

class FailingStep(ProcessStep):
    def __init__(self):
        self.executed = False
    
    @property
    def name(self) -> str:
        return "Failing test step."

    def execute(self, context):
        self.executed = True
        raise RuntimeError("boom")
    
def test_runner_stops_on_failure():
    runner = ProcessRunner()
    step1 = RecordingStep()
    step2 = FailingStep()
    step3 = RecordingStep()

    def make_payload(process_steps: list):
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
    runner = ProcessRunner()

    steps = [
        RecordingStep(),
        RecordingStep(),
    ]

    def make_payload(process_steps: list):
        return ProcessRunnerInput(
            ProcessDefinition("test", process_steps),
            ProcessContext(None, None)
            )

    payload = make_payload(steps)

    result = runner.run(payload)

    assert result.status is ProcessStatus.SUCCESS
    assert all(step.executed for step in steps)




