import pytest

from domain import (
    JobCreated,
    JobMovedToProcessing,
    JobMovedToVerifying,
    JobCompleted,
    JobStatus,
)

from application import (
    JobService,
    EventPublisher,
    EventEnvelope,
    JobVerifyingProcessManager,
    TranscodeVerified,
    TranscodeVerificationFailed,
)

from infrastructure import (
    SyncEventBus,
)

from tests import (
    FakeJobRepository,
    FakeFileSystem,
    JobFactory,
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

def test_job_verification_request_to_completion_happy_path():
    fs = FakeFileSystem()
    repo = FakeJobRepository()
    bus = SyncEventBus()
    publisher = EventPublisher(bus)
    service = JobService(repo, publisher)
    verifying_process_manager = JobVerifyingProcessManager(publisher, fs)

    emitted = []

    def capture(envelope):
        emitted.append(type(envelope.event))

    bus.subscribe(JobMovedToVerifying, capture)
    bus.subscribe(TranscodeVerified, capture)
    bus.subscribe(JobCompleted, capture)

    bus.subscribe(JobMovedToVerifying, verifying_process_manager)
    bus.subscribe(TranscodeVerified, service)

    job = JobFactory(status=JobStatus.processing)

    repo.save(job)
    fs.add(job.transcode_file)

    service.verify_job(job.id)

    assert emitted == [
        JobMovedToVerifying,
        TranscodeVerified,
        JobCompleted,
    ]