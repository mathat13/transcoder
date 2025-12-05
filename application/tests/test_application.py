from unittest.mock import MagicMock

from application import FakeEventBus, FakeJobRepository, FakeLogger, FakeFileSystem, JobService, FileChecker, EventBus
from domain import JobStatusChanged, JobFactory, JobCreated, JobStatus, JobTranscodeCompleted

def test_event_bus_calls_subscribers():
    bus = FakeEventBus()
    called = []

    def handler(event):
        called.append(event)

    bus.subscribe(JobStatusChanged, handler)

    evt = [JobStatusChanged(job_id=1, old_status=JobStatus.pending, new_status=JobStatus.success)]
    bus.publish_all(evt)

    assert called == evt

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
    print(bus.published)
    assert isinstance(bus.published[0], JobCreated)

    # subscriber
    assert len(handled) == 1

def test_subscriber_receives_domain_event():
    repo = FakeJobRepository()
    bus = FakeEventBus()

    received = []

    def subscriber(event):
        received.append(event)

    bus.subscribe(JobStatusChanged, subscriber)

    # store job
    job = JobFactory(id=1, status=JobStatus.pending)
    repo.save(job)

    service = JobService(repo, bus)
    service.transition_job(1, JobStatus.processing)

    assert len(received) == 1
    assert received[0].new_status == JobStatus.processing.value

def test_FileChecker_Full_workflow():
    fs = FakeFileSystem()
    logger = FakeLogger()
    fchecker = FileChecker(fs, logger)

    repo = FakeJobRepository()
    bus = EventBus()
    svc = JobService(repo, bus)

    bus.subscribe(JobCreated, fchecker)
    
    # JobCreated event emitted here
    svc.create_job("episode", "/input.mp4")

    assert len(logger.messages) == 1
    assert "Source OK" in logger.messages[0]

def test_FileChecker_successful_workflow():
    fs = FakeFileSystem()
    logger = FakeLogger()

    fchecker = FileChecker(fs, logger)

    # Simulate JobCreated event
    job_created_event = JobCreated(job_id=1, job_status=JobStatus.pending, source_path="/path/to/source.mp4")
    fchecker(job_created_event)

    assert len(logger.messages) == 1
    assert "Source OK" in logger.messages[0]

    # Simulate JobTranscodeCompleted event

    transcode_completed_event = JobTranscodeCompleted(job_id=1, output_path="/path/to/output.mp4")
    fchecker(transcode_completed_event)

    assert len(logger.messages) == 2
    assert "Output OK" in logger.messages[1]

def test_FileChecker_missing_files():
    fs = FakeFileSystem()
    logger = FakeLogger()

    fchecker = FileChecker(fs, logger)

    # Simulate JobCreated event with missing source
    job_created_event = JobCreated(job_id=1, job_status=JobStatus.pending, source_path="")
    fchecker(job_created_event)

    assert len(logger.errors) == 1
    assert "Source missing" in logger.errors[0]

    # Simulate JobTranscodeCompleted event with missing output

    transcode_completed_event = JobTranscodeCompleted(job_id=1, output_path="")
    fchecker(transcode_completed_event)

    assert len(logger.errors) == 2
    assert "Output missing" in logger.errors[1]

