import pytest
from typing import (List,
                    Type,
                    )

from tests.factories.JobFactory import JobFactory
from tests.factories.EventFactories import (
    JobMovedToProcessingEventFactory,
    JobMovedToVerifyingEventFactory,
    JobCompletedEventFactory,
    TranscodeVerifiedEventFactory,
    JobCompletionSuccessEventFactory,
    EventEnvelopeFactory,
)
from tests.bootstrap.Types import JobServiceTestSystem

from domain import (
    FileInfo,
    ExternalMediaIDs,
    Event,
    JobMovedToProcessing,
    JobMovedToVerifying,
    JobCompleted,
    JobFailed,
    JobStatus,
    OperationContext,
)

from application import (
    JobNotFoundDuringVerification,
    JobDispatched,
    NoJobAvailable,
    JobFound,
    VerificationStarted,
    JobCreatedResult,
    CreateJobCommand,
)
from application.services.jobs.commands.verify_job.results import JobNotFound as VerifyJobNotFound
from application.services.jobs.queries.get_job_by_id.results import JobNotFound as GetJobByIDNotFound

def test_JobService_emit_emits_events_correctly(job_service_test_system: JobServiceTestSystem):

    # Setup
    job = JobFactory(status=JobStatus.pending)
    context = OperationContext.create()
    job.events = [JobCompletedEventFactory(),
                  JobMovedToProcessingEventFactory(),
                  JobMovedToVerifyingEventFactory(),
                  ]
    
    # Execution
    job_service_test_system.job_service._emit(job, context)

    assert job_service_test_system.event_bus.processed_event_types() == [
        JobCompleted,
        JobMovedToProcessing,
        JobMovedToVerifying,
        ]
    
# Events

@pytest.mark.parametrize(
    "initial_status, request_status, expected_event_list",
    [
        # Add created job event check here!
        (JobStatus.pending, JobStatus.processing, [JobMovedToProcessing]),
        (JobStatus.processing, JobStatus.verifying, [JobMovedToVerifying]),
        (JobStatus.verifying, JobStatus.success, [JobCompleted]),
        (JobStatus.verifying, JobStatus.error, [JobFailed]),
        (JobStatus.processing, JobStatus.error, [JobFailed]),
    ],
)

def test_JobService_emits_correct_events_on_status_transition(initial_status: JobStatus,
                                                                                     request_status: JobStatus,
                                                                                     expected_event_list:List[Type[Event]],
                                                                                     job_service_test_system: JobServiceTestSystem
                                                                                     ):

    # Setup
    context = OperationContext.create()
    job = JobFactory(status=initial_status)

    # Execution
    job_service_test_system.job_service._transition_job(job, request_status)
    job_service_test_system.job_service._emit(job=job, context=context)
    assert job_service_test_system.event_bus.processed_event_types() == expected_event_list

def test_JobService_call_method_with_TranscodeVerified_event_emits_JobNotFoundDuringVerification_on_no_job_in_repo(job_service_test_system: JobServiceTestSystem):
    # Setup
    job = JobFactory(status=JobStatus.verifying)
    envelope = EventEnvelopeFactory(event=TranscodeVerifiedEventFactory(job_id=job.id))

    # Execution
    job_service_test_system.event_bus.publish(envelope=envelope)

    # Validation
    assert len(job_service_test_system.event_bus.processed_event_types(event_type=JobNotFoundDuringVerification)) == 1
    assert len(job_service_test_system.event_bus.processed_event_types(event_type=JobCompleted)) == 0

    assert job_service_test_system.event_bus.processed_events_of_type(event_type=JobNotFoundDuringVerification)[0].job_id == job.id

def test_JobService_call_method_with_TranscodeVerified_event_emits_JobCompleted_on_success(job_service_test_system: JobServiceTestSystem):

    # Setup
    job = JobFactory(status=JobStatus.verifying)
    job_service_test_system.job_repo.save(job)
    envelope = EventEnvelopeFactory(event=TranscodeVerifiedEventFactory(job_id=job.id))

    # Execution
    job_service_test_system.event_bus.publish(envelope=envelope)

    assert len(job_service_test_system.event_bus.processed_event_types(event_type=JobNotFoundDuringVerification)) == 0
    assert len(job_service_test_system.event_bus.processed_event_types(event_type=JobCompleted)) == 1

def test_JobService_call_method_with_JobCompletionSuccess_event_triggers_job_deletion(job_service_test_system: JobServiceTestSystem):

    # Setup
    job = JobFactory(status=JobStatus.verifying)
    job_service_test_system.job_repo.save(job)
    envelope = EventEnvelopeFactory(event=JobCompletionSuccessEventFactory(job_id=job.id))

    # Execution
    job_service_test_system.event_bus.publish(envelope=envelope)

    assert job_service_test_system.job_repo.get_job_by_id(job.id) is None

# Commands/ queries

def test_JobService_get_job_by_id_with_job_success(job_service_test_system: JobServiceTestSystem):
    # Setup
    job = JobFactory(status=JobStatus.pending)
    ctx = OperationContext.create()
    job_service_test_system.job_repo.save(job)

    # Execution
    result = job_service_test_system.job_service.get_job_by_id(id=job.id, ctx=ctx)

    # Verification
    assert isinstance(result, JobFound)
    assert result.job is job

def test_JobService_get_job_by_id_with_no_job(job_service_test_system: JobServiceTestSystem):
    # Setup
    job = JobFactory(status=JobStatus.pending)
    ctx = OperationContext.create()
    # No saving of job to repo

    # Execution
    result = job_service_test_system.job_service.get_job_by_id(id=job.id, ctx=ctx)

    # Verification
    assert isinstance(result, GetJobByIDNotFound)

def test_JobService_create_job_with_manual_command(job_service_test_system: JobServiceTestSystem):
    source_file=FileInfo.from_path("/media/input.mp4")
    cmd = CreateJobCommand.from_manual(source_file=source_file)
    ctx = OperationContext.create()

    result = job_service_test_system.job_service.create_job(cmd=cmd, ctx=ctx)

    assert isinstance(result, JobCreatedResult)
    assert result.job.external_media_ids is None
    assert result.job.source_file is source_file

def test_JobService_create_job_with_radarr_command(job_service_test_system: JobServiceTestSystem):
    source_file=FileInfo.from_path("/media/input.mp4")
    media_ids=ExternalMediaIDs.from_radarr(4)
    cmd = CreateJobCommand.from_radarr(source_file=source_file, media_ids=media_ids)
    ctx = OperationContext.create()
    
    result = job_service_test_system.job_service.create_job(cmd=cmd, ctx=ctx)

    assert isinstance(result, JobCreatedResult)
    assert result.job.external_media_ids is media_ids
    assert result.job.source_file is source_file

def test_JobService_dispatch_job_with_job(job_service_test_system: JobServiceTestSystem):
    # Setup
    job = JobFactory(status=JobStatus.pending)
    ctx = OperationContext.create()
    job_service_test_system.job_repo.save(job)

    # Execution
    result = job_service_test_system.job_service.dispatch_job(ctx=ctx)

    # Verification
    assert job_service_test_system.event_bus.processed_event_types() == [
        JobMovedToProcessing,
    ]

    retrieved_job = job_service_test_system.job_repo.get_job_by_id(job.id)
    assert retrieved_job.status == JobStatus.processing

    assert isinstance(result, JobDispatched)
    assert result.job is job

def test_JobService_dispatch_job_with_no_job(job_service_test_system: JobServiceTestSystem):
    # Setup
    job = JobFactory(status=JobStatus.pending)
    ctx = OperationContext.create()

    # Execution
    result = job_service_test_system.job_service.dispatch_job(ctx=ctx)

    # Verification
    assert job_service_test_system.event_bus.processed_event_types() == []
    
    retrieved_job = job_service_test_system.job_repo.get_job_by_id(job.id)
    assert retrieved_job is None

    assert isinstance(result, NoJobAvailable)

def test_JobService_verify_job_on_no_job_in_repo(job_service_test_system: JobServiceTestSystem):
    # Setup
    job = JobFactory(status=JobStatus.processing)
    job_id = job.id
    ctx = OperationContext.create()

    # Execution
    result = job_service_test_system.job_service.verify_job(id=id, ctx=ctx)

    # Validation
    assert isinstance(result, VerifyJobNotFound)
    assert job_service_test_system.job_repo.get_job_by_id(id=job.id) is None

def test_JobService_verify_job_returns_correctly(job_service_test_system: JobServiceTestSystem):
    # Setup
    job = JobFactory(status=JobStatus.processing)
    id = job.id
    ctx = OperationContext.create()
    job_service_test_system.job_repo.save(job=job)

    # Execution
    result = job_service_test_system.job_service.verify_job(id=id, ctx=ctx)

    # Validation
    assert isinstance(result, VerificationStarted)
    assert job_service_test_system.job_repo.get_job_by_id(id=job.id) is not None

    

