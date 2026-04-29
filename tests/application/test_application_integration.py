import pytest

from tests.factories.JobFactory import JobFactory
from tests.bootstrap.Types import ApplicationTestSystem

from domain import (
    JobCreated,
    JobMovedToProcessing,
    JobMovedToVerifying,
    JobCompleted,
    JobStatus,
    OperationContext,
    FileInfo,
)

from application import (
    TranscodeVerified,
    JobCompletionSuccess,
    JobDispatched,
    CreateJobCommand,
    VerificationStarted,
    CreateJobResult,
)

def test_manual_job_creation_happy_path(application_test_system: ApplicationTestSystem):
    # Setup
    cmd = CreateJobCommand.from_manual(source_file=FileInfo.from_path("/media/input.mp4"))
    ctx = OperationContext.create()

    # Execution
    result = application_test_system.job_service.create_job(cmd=cmd, ctx=ctx)

    # Verification
    assert application_test_system.event_bus.processed_event_types() == [
        JobCreated,
    ]

    assert issubclass(type(result), CreateJobResult)

def test_job_dispatch_request_happy_path(application_test_system: ApplicationTestSystem):
    # Setup
    job = JobFactory(status=JobStatus.pending)
    ctx = OperationContext.create()
    application_test_system.job_repo.save(job)

    # Execution
    result = application_test_system.job_service.dispatch_job(ctx=ctx)

    # Verification
    assert application_test_system.event_bus.processed_event_types() == [
        JobMovedToProcessing,
    ]

    assert isinstance(result, JobDispatched)

def test_job_verification_request_to_completion_happy_path(application_test_system: ApplicationTestSystem):
    # Setup
    job = JobFactory(status=JobStatus.processing)
    ctx = OperationContext.create()
    application_test_system.job_repo.save(job)
    application_test_system.filesystem.add(job.source_file.path)
    application_test_system.filesystem.add(job.transcode_output_file.path)
    application_test_system.radarr.add_movie(media_identifiers=job.external_media_ids,
                                             file=job.source_file,
                                             context=ctx)

    # Execute
    result = application_test_system.job_service.verify_job(job_id=job.id, ctx=ctx)

    # Verification
    assert application_test_system.event_bus.processed_event_types() == [
    JobMovedToVerifying,
    TranscodeVerified,
    JobCompleted,
    JobCompletionSuccess,
    ]

    assert isinstance(result, VerificationStarted)

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