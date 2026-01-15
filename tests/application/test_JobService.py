from domain import (
    JobCreated,
    JobMovedToProcessing,
    JobMovedToVerifying,
    JobCompleted,
    JobFailed,
    JobStatus,
)

from application import (
    EventPublisher,
    JobService,
)

from tests import (
    FakeJobRepository,
    FakeSyncEventBus,
    JobFactory,
)

def test_JobService_emits_correct_events_on_status_transition():
    bus = FakeSyncEventBus()
    repo = FakeJobRepository()
    publisher = EventPublisher(bus)
    svc = JobService(repo, publisher)

    handled = []

    def handler(envelope):
        handled.append(envelope)

    bus.subscribe(JobCreated, handler)
    bus.subscribe(JobMovedToProcessing, handler)
    bus.subscribe(JobMovedToVerifying, handler)
    bus.subscribe(JobCompleted, handler)
    bus.subscribe(JobFailed, handler)

    job = svc.create_job("/input.mp4", 5)
    assert isinstance(handled[0].event, JobCreated)

    svc.transition_job(job.id, JobStatus.processing)
    assert isinstance(handled[1].event, JobMovedToProcessing)

    svc.transition_job(job.id, JobStatus.verifying)
    assert isinstance(handled[2].event, JobMovedToVerifying)

    svc.transition_job(job.id, JobStatus.success)
    assert isinstance(handled[3].event, JobCompleted)

    # Save a new job to test failure transition 
    job2 = JobFactory(status=JobStatus.verifying)
    repo.save(job2)

    # Test failure transition
    svc.transition_job(job2.id, JobStatus.error)
    assert isinstance(handled[4].event, JobFailed)