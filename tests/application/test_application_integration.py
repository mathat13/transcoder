import pytest
from typing import (List,
                    Type,
                    )

from tests.fakes.FakeJobRepository import FakeJobRepository
from tests.factories.JobFactory import JobFactory
from tests.bootstrap.Types import ApplicationTestSystem

from domain import (
    JobCreated,
    JobMovedToProcessing,
    JobMovedToVerifying,
    JobCompleted,
    JobStatus,
    Event,
)

from application import (
    JobService,
    EventPublisher,
    EventEnvelope,
    TranscodeVerified,
)

from infrastructure import (
    SyncEventBus,
)

def test_job_creation_happy_path():
    repo = FakeJobRepository()
    bus = SyncEventBus()
    publisher = EventPublisher(bus)
    service = JobService(repo, publisher)

    emitted = []

    def capture(envelope):
        emitted.append(type(envelope.event))

    bus.subscribe(JobCreated, capture)
    
    service.create_job("/input.mp4", 4)

    assert emitted == [
        JobCreated,
    ]

def test_job_process_request_happy_path():
    repo = FakeJobRepository()
    bus = SyncEventBus()
    publisher = EventPublisher(bus)
    service = JobService(repo, publisher)

    emitted = []

    def capture(envelope):
        emitted.append(type(envelope.event))

    bus.subscribe(JobMovedToProcessing, capture)

    job = JobFactory(status=JobStatus.pending)

    repo.save(job)

    service._transition_job(job=job, new_status=JobStatus.processing)

    assert emitted == [
        JobMovedToProcessing,
    ]

def test_job_verification_request_to_completion_happy_path(application_test_system: ApplicationTestSystem):

    handled: List[Type[Event]] = []

    def handler(envelope: EventEnvelope) -> None:
        handled.append(type(envelope.event))

    application_test_system.event_bus.subscribe(event_type=JobMovedToVerifying, handler=handler)
    application_test_system.event_bus.subscribe(event_type=TranscodeVerified, handler=handler)
    application_test_system.event_bus.subscribe(event_type=JobCompleted, handler=handler)

    job = JobFactory(status=JobStatus.processing)

    application_test_system.job_repo.save(job)
    application_test_system.filesystem.add(job.transcode_file.path)

    application_test_system.job_service.verify_job(job.id)

    # List reversed due to order of execution in sync workflows
    assert list(reversed(handled)) == [
    JobMovedToVerifying,
    TranscodeVerified,
    JobCompleted,
]