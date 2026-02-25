from uuid import uuid4
from typing import (
    Type,
    List,
)

from domain import (
    JobCreated,
    JobMovedToProcessing,
    JobMovedToVerifying,
    JobCompleted,
    JobFailed,
    JobStatus,
    OperationContext,
    FileInfo,
    ExternalMediaIDs,
    Event,
)

from application import (
    EventEnvelope,
)

from tests.factories.JobFactory import JobFactory
from tests.factories.EventFactories import (
    JobMovedToProcessingEventFactory,
    JobMovedToVerifyingEventFactory,
    JobCompletedEventFactory,
    TranscodeVerifiedEventFactory,
    EventEnvelopeFactory,
)
from tests.bootstrap.Types import JobServiceTestSystem

def test_JobService_emits_correct_events_on_status_transition(job_service_test_system: JobServiceTestSystem):

    handled: List[EventEnvelope] = []

    def handler(envelope: EventEnvelope):
        handled.append(envelope)

    job_service_test_system.event_bus.subscribe(JobCreated, handler)
    job_service_test_system.event_bus.subscribe(JobMovedToProcessing, handler)
    job_service_test_system.event_bus.subscribe(JobMovedToVerifying, handler)
    job_service_test_system.event_bus.subscribe(JobCompleted, handler)
    job_service_test_system.event_bus.subscribe(JobFailed, handler)

    # Add created job event check here!

    pending_job = JobFactory(status=JobStatus.pending)
    job_service_test_system.job_service._transition_job(pending_job, JobStatus.processing)
    assert isinstance(pending_job.events[0], JobMovedToProcessing)

    processing_job = JobFactory(status=JobStatus.processing)
    job_service_test_system.job_service._transition_job(processing_job, JobStatus.verifying)
    assert isinstance(processing_job.events[0], JobMovedToVerifying)

    verifying_job = JobFactory(status=JobStatus.verifying)
    job_service_test_system.job_service._transition_job(verifying_job, JobStatus.success)
    assert isinstance(verifying_job.events[0], JobCompleted)

    # Test failure transitions
    verifying_job = JobFactory(status=JobStatus.verifying)
    job_service_test_system.job_service._transition_job(verifying_job, JobStatus.error)
    assert isinstance(verifying_job.events[0], JobFailed)

    processing_job = JobFactory(status=JobStatus.processing)
    job_service_test_system.job_service._transition_job(processing_job, JobStatus.error)
    assert isinstance(processing_job.events[0], JobFailed)

def test_JobService_call_method_with_TranscodeVerified_event_emits_JobCompleted_on_success(job_service_test_system: JobServiceTestSystem):

    handled: List[Type[Event]] = []

    def handler(envelope: EventEnvelope):
        handled.append(type(envelope.event))

    # Setup
    job = JobFactory(status=JobStatus.verifying)
    job_service_test_system.job_repo.save(job)

    job_service_test_system.event_bus.subscribe(JobCompleted, handler)

    envelope=EventEnvelopeFactory(
        event=TranscodeVerifiedEventFactory(
        job_id=job.id,
        transcode_file=job.transcode_file
        )
    )

    job_service_test_system.event_bus.publish(envelope=envelope)

    assert handled == [
        JobCompleted,
    ]

def test_JobService_emit_emits_events_correctly(job_service_test_system: JobServiceTestSystem):

    handled: List[Type[Event]] = []

    def handler(envelope: EventEnvelope):
        handled.append(type(envelope.event))
    
    job = JobFactory(status=JobStatus.pending)
    context = OperationContext.create()

    job_service_test_system.event_bus.subscribe(JobCompleted, handler)
    job_service_test_system.event_bus.subscribe(JobMovedToProcessing, handler)
    job_service_test_system.event_bus.subscribe(JobMovedToVerifying, handler)
    
    job.events = [JobCompletedEventFactory(),
                  JobMovedToProcessingEventFactory(),
                  JobMovedToVerifyingEventFactory(),
                  ]
    job_service_test_system.job_service._emit(job, context)

    assert job_service_test_system.event_bus.published == [
        JobCompleted,
        JobMovedToProcessing,
        JobMovedToVerifying,
        ]
    

