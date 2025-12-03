from unittest.mock import MagicMock

from application import FakeEventBus, FakeJobRepository, JobService
from domain import JobStatusChanged, JobFactory, JobCreated, JobStatus

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