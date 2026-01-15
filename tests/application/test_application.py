from domain import (
    JobCreated,
)

from application import (
    JobService,
    EventPublisher,
    EventEnvelope,
    JobVerifyingProcessManager,
)

from infrastructure import (
    SyncEventBus,
)

from tests import (
    FakeSyncEventBus,
    FakeJobRepository,
    FakeFileSystem,
)

def test_job_state_change_calls_subscribers_correctly():
    repo = FakeJobRepository()
    bus = SyncEventBus()
    publisher = EventPublisher(bus)
    service = JobService(repo, publisher)

    handled = []

    def handler(envelope):
        handled.append(envelope)

    bus.subscribe(JobCreated, handler)
    
    service.create_job("/input.mp4", 4)

    assert len(handled) == 1
    assert isinstance(handled[0], EventEnvelope)
    event = handled[0].event
    assert isinstance(event, JobCreated)