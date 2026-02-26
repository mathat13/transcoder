import pytest

from tests.factories.JobFactory import JobFactory
from tests.bootstrap.Types import ApplicationTestSystem

from domain import (
    JobCreated,
    JobMovedToProcessing,
    JobMovedToVerifying,
    JobCompleted,
    JobStatus,
)

from application import (
    TranscodeVerified,
    JobCompletionSuccess,
)

def test_job_creation_happy_path(application_test_system: ApplicationTestSystem):
    application_test_system.job_service.create_job("/input.mp4", 4)

    assert application_test_system.event_bus.processed_event_types == [
        JobCreated,
    ]

def test_job_process_request_happy_path(application_test_system: ApplicationTestSystem):
    job = JobFactory(status=JobStatus.pending)

    application_test_system.job_repo.save(job)

    application_test_system.job_service._transition_job(job=job, new_status=JobStatus.processing)

    assert application_test_system.event_bus.processed_event_types == [
        JobMovedToProcessing,
    ]

def test_job_verification_request_to_completion_happy_path(application_test_system: ApplicationTestSystem):

    # Setup for happy path
    job = JobFactory(status=JobStatus.processing)
    application_test_system.job_repo.save(job)
    application_test_system.filesystem.add(job.transcode_file.path)

    # Execute
    application_test_system.job_service.verify_job(job.id)

    # Assert specific order of operation
    assert application_test_system.event_bus.processed_event_types == [
    JobMovedToVerifying,
    TranscodeVerified,
    JobCompleted,
    JobCompletionSuccess,
    ]

    # Assert specific events processed (Example)
    assert {
    JobMovedToVerifying,
    TranscodeVerified,
    JobCompleted,
    JobCompletionSuccess,
}.issubset(set(application_test_system.event_bus.processed_event_types))