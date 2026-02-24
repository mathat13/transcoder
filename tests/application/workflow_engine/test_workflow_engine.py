import pytest

from application import (
    FailureClassifier,
    FailureInfo,
    ProcessRunnerResult,
    ProcessStatus,
    FailureReason,
    FileSystemFileMissing,
    FileSystemIOError,
    APIServiceRetryableException,
    APIServiceTerminalException,
    RetryableException,
    TerminalException,
)

def test_ProcessRunnerResult_generates_correct_success_response():
    success_response = ProcessRunnerResult.success()

    assert isinstance(success_response, ProcessRunnerResult)
    assert success_response.status == ProcessStatus.SUCCESS
    assert success_response.failure_info == None

@pytest.mark.parametrize(
    "exception, expected_reason",
    [
        (FileSystemFileMissing("/file.mp4"), FailureReason.FILESYSTEM_LOGIC),
        (FileSystemIOError("hardlink", "/file.mp4", OSError), FailureReason.FILESYSTEM_IO),
        (APIServiceRetryableException("Radarr", 500, None), FailureReason.API_CALL_FAILURE),
        (APIServiceTerminalException("Radarr", 404, None), FailureReason.API_CALL_FAILURE),
        (OverflowError(), FailureReason.UNKNOWN),
    ],
)

def test_FailureClassifier_classifies_exceptions_correctly(exception: Exception, expected_reason: FailureReason):
    classifier = FailureClassifier()

    failure_info = classifier.classify(exception)

    assert failure_info.reason == expected_reason
    assert failure_info.detail == str(exception)
    if isinstance(exception, RetryableException):
            assert failure_info.retryable == True
    elif isinstance(exception, TerminalException):
        assert failure_info.retryable == False
    else:
        assert failure_info.retryable == False

@pytest.mark.parametrize(
    "exception, expected_reason",
    [
        (FileSystemFileMissing("/file.mp4"), FailureReason.FILESYSTEM_LOGIC),
        (FileSystemIOError("hardlink", "/file.mp4", OSError), FailureReason.FILESYSTEM_IO),
        (APIServiceRetryableException("Radarr", 500, None), FailureReason.API_CALL_FAILURE),
        (APIServiceTerminalException("Radarr", 404, None), FailureReason.API_CALL_FAILURE),
        (OverflowError(), FailureReason.UNKNOWN),
    ],
)

def test_ProcessRunnerResult_generates_correct_failure_response(exception: Exception, expected_reason: FailureReason):

    classifier = FailureClassifier()

    failure_response_without_classifier_param = ProcessRunnerResult.failure(exc=exception)
    failure_response_with_classifier_param = ProcessRunnerResult.failure(exc=exception, classifier=classifier)

    for failure_response in [failure_response_without_classifier_param, failure_response_with_classifier_param]:
        assert isinstance(failure_response, ProcessRunnerResult)
        assert failure_response.status == ProcessStatus.FAILURE

        # failure_info
        failure = failure_response.failure_info
        assert isinstance(failure, FailureInfo)
