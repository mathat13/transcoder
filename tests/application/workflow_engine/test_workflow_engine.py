import pytest

from domain import OperationContext

from application import (
    FailureClassifier,
    FailureInfo,
    ProcessRunnerResult,
    ProcessStatus,
    FailureReason,
    SourceFileMissing,
    FileSystemIOError,
    APIServiceException,
    ProcessContext,
    EventEnvelope,
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


