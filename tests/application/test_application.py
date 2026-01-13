from uuid import uuid4

from infrastructure import SyncEventBus

from application import (
    JobService,
    JobVerifyingOrchestrator,
    TranscodeVerified,
    TranscodeVerificationFailed,
    EventPublisher,
    EventEnvelope,
)
from domain import (
    JobStatusChanged,
    JobCreated,
    JobMovedToProcessing,
    JobMovedToVerifying,
    JobCompleted,
    JobFailed,
    JobStatus,
    FileInfo,
    OperationContext,
)

from tests import (
    FakeSyncEventBus,
    FakeJobRepository,
    FakeLogger,
    FakeFileSystem,
    JobFactory
)



def test_JobService_emits_correct_events_on_status_transition():
    bus = SyncEventBus()
    repo = FakeJobRepository()

    svc = JobService(repo, bus)

    handled = []

    def handler(envelope):
        handled.append(envelope)

    bus.subscribe(JobCreated, handler)
    bus.subscribe(JobMovedToProcessing, handler)
    bus.subscribe(JobMovedToVerifying, handler)
    bus.subscribe(JobCompleted, handler)
    bus.subscribe(JobFailed, handler)

    job = svc.create_job("/input.mp4", 5)
    assert isinstance(handled[0], JobCreated)

    svc.transition_job(job.id, JobStatus.processing)
    assert isinstance(handled[1], JobMovedToProcessing)

    svc.transition_job(job.id, JobStatus.verifying)
    assert isinstance(handled[2], JobMovedToVerifying)

    svc.transition_job(job.id, JobStatus.success)
    assert isinstance(handled[3], JobCompleted)

    # Save a new job to test failure transition 
    job2 = JobFactory(status=JobStatus.verifying)
    repo.save(job2)

    # Test failure transition
    svc.transition_job(job2.id, JobStatus.error)
    assert isinstance(handled[4], JobFailed)


def test_event_bus_calls_subscribers():
    bus = FakeSyncEventBus()
    handled = []

    def handler(envelope):
        handled.append(envelope)

    bus.subscribe(JobStatusChanged, handler)

    evt = JobStatusChanged(job_id=uuid4(), old_status=JobStatus.pending, new_status=JobStatus.success)
    context = OperationContext.create()
    envelope = EventEnvelope.create(evt, context)
    # Should not raise
    bus.publish(envelope)

    assert envelope in handled

def test_event_bus_no_subscribers():
    bus = FakeSyncEventBus()

    evt = JobStatusChanged(job_id=uuid4(), old_status=JobStatus.pending, new_status=JobStatus.success)
    context = OperationContext.create()
    envelope = EventEnvelope.create(evt, context)
    # Should not raise
    bus.publish(envelope)

def test_event_bus_publish_called_directly():
    bus = FakeSyncEventBus()
    handled = []
    bus.subscribe(JobStatusChanged, lambda evt: handled.append(evt))

    evt = JobStatusChanged(job_id=uuid4(), old_status=JobStatus.pending, new_status=JobStatus.success)
    context = OperationContext.create()
    envelope = EventEnvelope.create(evt, context)
    # Should not raise
    bus.publish(envelope)

    assert envelope in handled

def test_creating_a_job_emits_event_and_saves_to_repo():
    repo = FakeJobRepository()
    bus = FakeSyncEventBus()

    handled = []

    def handler(envelope):
        handled.append(envelope)

    bus.subscribe(JobCreated, handler)

    svc = JobService(repo, bus)

    job = svc.create_job("/input.mp4", 5)

    # repo
    saved = repo._get_job_by_id(job.id)
    assert saved.id == job.id
    assert saved.source_file == job.source_file
    assert saved.status == job.status
    assert saved.external_media_ids == job.external_media_ids

    # domain events
    assert len(job.events) == 0         # cleared after publish
    assert isinstance(bus.published[0], JobCreated)

    # subscriber
    assert len(handled) == 1

def test_subscriber_receives_domain_event():
    repo = FakeJobRepository()
    bus = FakeSyncEventBus()
    service = JobService(repo, bus)

    handled = []

    def handler(envelope):
        handled.append(envelope)

    bus.subscribe(JobMovedToVerifying, handler)
    
    # store job
    job = JobFactory(status=JobStatus.processing)
    repo.save(job)

    service.transition_job(job.id, JobStatus.verifying)

    assert len(handled) == 1
    event = bus.published[0]
    assert isinstance(event, JobMovedToVerifying)
    assert event.job_id == job.id

def test_JobVerifyingOrchestrator_unit_test():
    fs = FakeFileSystem()
    bus = FakeSyncEventBus()
    logger = FakeLogger()
    orchestrator = JobVerifyingOrchestrator(bus, logger, fs)
    handled = []

    def handler(envelope):
        handled.append(envelope)
    
    bus.subscribe(TranscodeVerified, handler)
    bus.subscribe(TranscodeVerificationFailed, handler)

    # Simulate JobMovedToVerifying event with existing file
    event = JobMovedToVerifying(job_id=uuid4(), transcode_file=FileInfo("/path/to/existing_file.mp4"))

    fs.add(event.transcode_file) # Add file to fake FS

    orchestrator(event)

    assert any(isinstance(evt, TranscodeVerified) for evt in handled)
    assert not any(isinstance(evt, TranscodeVerificationFailed) for evt in handled)

def test_JobVerifyingOrchestrator_integration():
    fs = FakeFileSystem()
    bus = SyncEventBus()
    logger = FakeLogger()
    repo = FakeJobRepository()

    svc = JobService(repo, bus)
    orchestrator = JobVerifyingOrchestrator(bus, logger, fs)

    handled = []

    def handler(envelope):
        handled.append(envelope)

    bus.subscribe(JobMovedToVerifying, orchestrator)
    bus.subscribe(TranscodeVerified, handler)
    bus.subscribe(TranscodeVerificationFailed, handler)

    job = svc.create_job("/input.mp4", 5)

    fs.add(job.transcode_file)

    svc.transition_job(job.id, JobStatus.processing)
    svc.transition_job(job.id, JobStatus.verifying)

    assert any(isinstance(evt, TranscodeVerified) for evt in handled)

def test_EventPublisher_generates_envelope_correctly():
    event_bus = FakeSyncEventBus()
    publisher = EventPublisher(event_bus)
    domain_event = JobMovedToVerifying(job_id=uuid4(), transcode_file=FileInfo("/path/to/existing_file.mp4"))
    context = OperationContext.create()
    envelope = publisher.create_envelope(domain_event, context)

    assert envelope.operation_id == context.operation_id
    assert isinstance(envelope.event, type(domain_event))
    assert envelope.operation_id is context.operation_id
    assert isinstance(envelope, EventEnvelope)

def test_EventPublisher_publish_publishes_correctly():
    handled = []

    def handler(envelope):
        handled.append(envelope)
    
    event_bus = FakeSyncEventBus()
    publisher = EventPublisher(event_bus)

    event_bus.subscribe(JobMovedToVerifying, handler)
    
    domain_event = JobMovedToVerifying(job_id=uuid4(), transcode_file=FileInfo("/path/to/existing_file.mp4"))
    context = OperationContext.create()
    publisher.publish(domain_event, context)

    assert isinstance(handled[0], EventEnvelope)