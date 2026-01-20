from uuid import uuid4

from domain import (
    FileInfo,
    OperationContext,
    JobStatus,
    JobMovedToVerifying,
)

from application import (
    EventPublisher,
    JobVerifyingProcessManager,
    TranscodeVerified,
    TranscodeVerificationFailed,
    JobService,
    EventEnvelope,
)

from infrastructure import (
    SyncEventBus,
)

from tests import (
    FakeFileSystem,
    FakeSyncEventBus,
    FakeJobRepository,
)

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

    fs.add(envelope.event.transcode_file.path) # Add file to fake FS

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

