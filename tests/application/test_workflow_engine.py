import pytest

from application import (
    FailureClassifier,
    FailureInfo,
    FailureReason,
    SourceFileMissing,
    FileSystemIOError,
    APIServiceException,
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

def test_failure_classifier_classifies_exceptions_correctly(exception, expected_reason):
    classifier = FailureClassifier()

    # Ensure retryable exists for UNKNOWN case
    if not hasattr(exception, "retryable"):
        exception.retryable = False
        
    failure_info = classifier.classify(exception)

    assert failure_info.reason == expected_reason
    assert failure_info.retryable == exception.retryable
    assert failure_info.detail == str(exception)


