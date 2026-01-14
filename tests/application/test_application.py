from uuid import uuid4
from unittest.mock import Mock

from infrastructure import SyncEventBus

from application import (
    JobService,
    JobVerifyingProcessManager,
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
    FakeFileSystem,
    JobFactory,
)



def test_JobService_emits_correct_events_on_status_transition():
    bus = SyncEventBus()
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
    publisher = EventPublisher(bus)
    svc = JobService(repo, publisher)

    handled = []

    def handler(envelope):
        handled.append(envelope)

    bus.subscribe(JobCreated, handler)


    job = svc.create_job("/input.mp4", 5)

    # repo
    saved = repo._get_job_by_id(job.id)
    assert saved.id == job.id
    assert saved.source_file == job.source_file
    assert saved.status == job.status
    assert saved.external_media_ids == job.external_media_ids

    # domain events
    assert len(job.events) == 0         # cleared after publish
    assert isinstance(bus.published[0].event, JobCreated)

    # subscriber
    assert len(handled) == 1

def test_subscriber_receives_domain_event():
    repo = FakeJobRepository()
    bus = FakeSyncEventBus()
    publisher = EventPublisher(bus)
    service = JobService(repo, publisher)

    handled = []

    def handler(envelope):
        handled.append(envelope)

    bus.subscribe(JobMovedToVerifying, handler)
    
    # store job
    job = JobFactory(status=JobStatus.processing)
    repo.save(job)

    service.transition_job(job.id, JobStatus.verifying)

    assert len(handled) == 1
    event = bus.published[0].event
    assert isinstance(event, JobMovedToVerifying)
    assert event.job_id == job.id

def test_JobVerifyingProcessManager_generates_correct_event_on_transcode_success():
    fs = FakeFileSystem()
    bus = FakeSyncEventBus()
    publisher = EventPublisher(bus)
    ProcessManager = JobVerifyingProcessManager(publisher, fs)
    handled = []

    def handler(envelope):
        handled.append(envelope)
    
    bus.subscribe(TranscodeVerified, handler)
    bus.subscribe(TranscodeVerificationFailed, handler)

    # Simulate JobMovedToVerifying event with existing file
    context = OperationContext.create()
    event = JobMovedToVerifying(job_id=uuid4(), transcode_file=FileInfo("/path/to/existing_file.mp4"))
    envelope = EventEnvelope.create(event=event, context=context)

    fs.add(envelope.event.transcode_file) # Add file to fake FS

    ProcessManager(envelope)

    assert any(isinstance(envelope.event, TranscodeVerified) for envelope in handled)
    assert not any(isinstance(envelope.event, TranscodeVerificationFailed) for envelope in handled)

def test_JobVerifyingProcessManager_generates_correct_event_on_transcode_failure():
    fs = FakeFileSystem()
    bus = FakeSyncEventBus()
    publisher = EventPublisher(bus)
    ProcessManager = JobVerifyingProcessManager(publisher, fs)
    handled = []

    def handler(envelope):
        handled.append(envelope)
    
    bus.subscribe(TranscodeVerified, handler)
    bus.subscribe(TranscodeVerificationFailed, handler)

    # Simulate JobMovedToVerifying event with existing file
    context = OperationContext.create()
    event = JobMovedToVerifying(job_id=uuid4(), transcode_file=FileInfo("/path/to/existing_file.mp4"))
    envelope = EventEnvelope.create(event=event, context=context)

    # No file added to fake fs

    ProcessManager(envelope)

    assert not any(isinstance(envelope.event, TranscodeVerified) for envelope in handled)
    assert any(isinstance(envelope.event, TranscodeVerificationFailed) for envelope in handled)

def test_job_verifying_process_manager_is_called_on_subscribed_event():
    bus = SyncEventBus()
    process_manager = Mock()

    bus.subscribe(JobMovedToVerifying, process_manager)

    envelope = EventEnvelope(
        event=JobMovedToVerifying(job_id=uuid4(), transcode_file="file.mkv"),
        context=OperationContext.create(),
    )

    bus.publish(envelope)

    process_manager.assert_called_once_with(envelope)

def test_job_verifying_process_manager_is_not_called_on_unsubscribed_event():
    bus = SyncEventBus()
    process_manager = Mock()

    bus.subscribe(JobMovedToVerifying, process_manager)

    envelope = EventEnvelope.create(
        event=JobCreated(job_id=uuid4(), source_file="file.mkv"),
        context=OperationContext.create(),
    )

    bus.publish(envelope)

    process_manager.assert_not_called()

def test_JobVerifyingProcessManager_integration():
    fs = FakeFileSystem()
    bus = SyncEventBus()
    publisher = EventPublisher(bus)
    repo = FakeJobRepository()

    svc = JobService(repo, publisher)
    ProcessManager = JobVerifyingProcessManager(publisher, fs)

    handled = []

    def handler(envelope):
        handled.append(envelope)

    bus.subscribe(JobMovedToVerifying, ProcessManager)
    bus.subscribe(TranscodeVerified, handler)
    bus.subscribe(TranscodeVerificationFailed, handler)

    job = svc.create_job("/input.mp4", 5)

    fs.add(job.transcode_file)

    svc.transition_job(job.id, JobStatus.processing)
    svc.transition_job(job.id, JobStatus.verifying)

    assert isinstance(handled[0].event, TranscodeVerified)
    assert any(isinstance(envelope.event, TranscodeVerified) for envelope in handled)

def test_EventPublisher_generates_envelope_correctly():
    event_bus = FakeSyncEventBus()
    publisher = EventPublisher(event_bus)
    domain_event = JobMovedToVerifying(job_id=uuid4(), transcode_file=FileInfo("/path/to/existing_file.mp4"))
    context = OperationContext.create()
    envelope = publisher.create_envelope(domain_event, context)

    assert envelope.context == context
    assert isinstance(envelope.event, type(domain_event))
    assert envelope.context is context
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