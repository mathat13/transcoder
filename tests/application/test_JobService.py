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
    EventEnvelopeFactory,
)
from tests.bootstrap.Types import JobServiceTestSystem

from domain import (
    Event,
    JobMovedToProcessing,
    JobMovedToVerifying,
    JobCompleted,
    JobFailed,
    JobStatus,
    OperationContext,
)

from application import (
    TranscodeVerified,
)

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

def test_JobService_emits_JobMovedToProcessing_event_on_processing_status_transition(initial_status: JobStatus,
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

def test_JobService_call_method_with_TranscodeVerified_event_emits_JobCompleted_on_success(job_service_test_system: JobServiceTestSystem):

    # Setup
    job = JobFactory(status=JobStatus.verifying)
    job_service_test_system.job_repo.save(job)
    envelope=EventEnvelopeFactory(
        event=TranscodeVerifiedEventFactory(
        job_id=job.id,
        transcode_file=job.transcode_file,
        )
    )

    # Execution
    job_service_test_system.event_bus.publish(envelope=envelope)

    assert len(job_service_test_system.event_bus.processed_event_types(event_type=JobCompleted)) == 1
    

