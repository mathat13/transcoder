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

@pytest.mark.integration
def test_job_moved_to_verifying_emits_TranscodeVerified_on_success():
    fs = FakeFileSystem()
    repo = FakeJobRepository()
    bus = SyncEventBus()
    publisher = EventPublisher(bus)
    service = JobService(repo, publisher)
    process_manager = JobVerifyingProcessManager(publisher, fs)

    handled = []

    def handler(envelope):
        handled.append(envelope)

    bus.subscribe(JobMovedToVerifying, process_manager)
    bus.subscribe(TranscodeVerified, handler)

    job = JobFactory(status=JobStatus.processing)

    repo.save(job)
    fs.add(job.transcode_file)

    service.transition_job(job.id, JobStatus.verifying)

    assert len(handled) == 1
    assert isinstance(handled[0], EventEnvelope)
    event = handled[0].event
    assert isinstance(event, TranscodeVerified)

@pytest.mark.integration
def test_job_moved_to_verifying_emits_TranscodeVerificationFailed_on_failure():
    fs = FakeFileSystem()
    repo = FakeJobRepository()
    bus = SyncEventBus()
    publisher = EventPublisher(bus)
    service = JobService(repo, publisher)
    process_manager = JobVerifyingProcessManager(publisher, fs)

    handled = []

    def handler(envelope):
        handled.append(envelope)

    bus.subscribe(JobMovedToVerifying, process_manager)
    bus.subscribe(TranscodeVerificationFailed, handler)

    job = JobFactory(status=JobStatus.processing)

    repo.save(job)
    # No fs.save(job) to fail verification

    service.transition_job(job.id, JobStatus.verifying)

    assert len(handled) == 1
    assert isinstance(handled[0], EventEnvelope)
    event = handled[0].event
    assert isinstance(event, TranscodeVerificationFailed)

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

    service.transition_job(job_id=job.id, new_status=JobStatus.processing)

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

    job = JobFactory(status=JobStatus.processing)

    repo.save(job)
    fs.add(job.transcode_file)

    service.transition_job(job.id, JobStatus.verifying)
    service.transition_job(job.id, JobStatus.success)

    assert emitted == [
        JobMovedToVerifying,
        TranscodeVerified,
        JobCompleted,
    ]