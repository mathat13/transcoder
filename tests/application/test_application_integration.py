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
    JobDispatched,
)

def test_job_creation_happy_path(application_test_system: ApplicationTestSystem):
    application_test_system.job_service.create_job(source="/media/input.mp4",
                                                   transcode_output_location="/transcode/transcode.mp4",
                                                   media_ids=4)

    assert application_test_system.event_bus.processed_event_types() == [
        JobCreated,
    ]

def test_job_process_request_happy_path(application_test_system: ApplicationTestSystem):
    job = JobFactory(status=JobStatus.pending)

    application_test_system.job_repo.save(job)

    result = application_test_system.job_service.dispatch_job()

    assert application_test_system.event_bus.processed_event_types() == [
        JobMovedToProcessing,
    ]

    assert isinstance(result, JobDispatched)

def test_job_verification_request_to_completion_happy_path(application_test_system: ApplicationTestSystem):

    # Setup for happy path
    job = JobFactory(status=JobStatus.processing)
    application_test_system.job_repo.save(job)
    application_test_system.filesystem.add(job.source_file.path)
    application_test_system.filesystem.add(job.transcode_output_file.path)
    application_test_system.radarr.add_movie(media_identifiers=job.external_media_ids,
                                             file=job.source_file,
                                             context=None)

    # Execute
    application_test_system.job_service.verify_job(job.id)

    # Assert specific order of operation
    assert application_test_system.event_bus.processed_event_types() == [
    JobMovedToVerifying,
    TranscodeVerified,
    JobCompleted,
    JobCompletionSuccess,
    ]

    # Assert job removed from repo
    assert application_test_system.job_repo.get_job_by_id(job.id) is None

    # Assert specific events processed (Example)
    assert {
    JobMovedToVerifying,
    TranscodeVerified,
}.issubset(application_test_system.event_bus.processed_event_types(event_type=(
    JobMovedToVerifying,
    TranscodeVerified,
    JobCompleted,
    JobCompletionSuccess,
    )))