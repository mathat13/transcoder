from unittest.mock import MagicMock

from application import (
    FakeEventBus,
    FakeJobRepository,
    FakeLogger,
    FakeFileSystem,
    JobService,
    EventBus,
    JobVerifyingOrchestrator,
    TranscodeVerified,
    TranscodeVerificationFailed
)
from domain import (
    JobStatusChanged,
    JobFactory,
    JobCreated,
    JobStatus,
    FileInfo,
    JobMovedToVerifying
)

def test_JobService_emits_correct_events_on_status_transition():
    pass

def test_event_bus_calls_subscribers():
    bus = FakeEventBus()
    called = []

    def handler(event):
        called.append(event)

    bus.subscribe(JobStatusChanged, handler)

    evt = [JobStatusChanged(job_id=1, old_status=JobStatus.pending, new_status=JobStatus.success)]
    bus.publish_all(evt)

    assert called == evt

def test_event_bus_no_subscribers():
    bus = FakeEventBus()

    evt = JobStatusChanged(job_id=1, old_status=JobStatus.pending, new_status=JobStatus.success)

    # Should not raise
    bus.publish(evt)

def test_event_bus_publish_called_directly():
    bus = FakeEventBus()
    handled = []
    bus.subscribe(JobStatusChanged, lambda evt: handled.append(evt))

    evt = JobStatusChanged(job_id=1, old_status=JobStatus.pending, new_status=JobStatus.success)
    bus.publish(evt)

    assert evt in handled

def test_creating_a_job_emits_event_and_saves_to_repo():
    repo = FakeJobRepository()
    bus = FakeEventBus()

    handled = []
    bus.subscribe(JobCreated, lambda evt: handled.append(evt))

    svc = JobService(repo, bus)

    job = svc.create_job("episode", "/input.mp4")

    # repo
    saved = repo.get(job.id)
    assert saved.id == job.id
    assert saved.source_path == job.source_path
    assert saved.status == job.status
    assert saved.job_type == job.job_type

    # domain events
    assert len(job.events) == 0         # cleared after publish
    assert isinstance(bus.published[0], JobCreated)

    # subscriber
    assert len(handled) == 1

def test_subscriber_receives_domain_event():
    repo = FakeJobRepository()
    bus = FakeEventBus()
    service = JobService(repo, bus)

    received = []

    def subscriber(event):
        received.append(event)

    bus.subscribe(JobMovedToVerifying, subscriber)
    
    # store job
    job = JobFactory(id=1, status=JobStatus.processing)
    repo.save(job)

    service.transition_job(1, JobStatus.verifying)

    assert len(received) == 1
    event = bus.published[0]
    assert isinstance(event, JobMovedToVerifying)
    assert event.job_id == job.id

def test_JobVerifyingOrchestrator_unit_test():
    fs = FakeFileSystem()
    bus = FakeEventBus()
    logger = FakeLogger()
    orchestrator = JobVerifyingOrchestrator(bus, logger, fs)
    handled = []

    def transcode_verified_handler(event):
        handled.append(event)
    
    bus.subscribe(TranscodeVerified, transcode_verified_handler)
    bus.subscribe(TranscodeVerificationFailed, transcode_verified_handler)

    # Simulate JobMovedToVerifying event with existing file
    event = JobMovedToVerifying(job_id=1, output_path=FileInfo("/path/to/existing_file.mp4"))
    orchestrator(event)

    assert any(isinstance(evt, TranscodeVerified) for evt in handled)
    assert not any(isinstance(evt, TranscodeVerificationFailed) for evt in handled)


def test_JobVerifyingOrchestrator_integration():
    fs = FakeFileSystem()
    bus = EventBus()
    logger = FakeLogger()
    repo = FakeJobRepository()

    svc = JobService(repo, bus)
    orchestrator = JobVerifyingOrchestrator(bus, logger, fs)

    handled = []

    def transcode_verified_handler(event):
        handled.append(event)

    bus.subscribe(JobMovedToVerifying, orchestrator)
    bus.subscribe(TranscodeVerified, transcode_verified_handler)
    bus.subscribe(TranscodeVerificationFailed, transcode_verified_handler)

    job = svc.create_job("episode", "/input.mp4")
    svc.transition_job(job.id, JobStatus.processing)
    svc.transition_job(job.id, JobStatus.verifying)

    print(handled)
    assert any(isinstance(evt, TranscodeVerified) for evt in handled)