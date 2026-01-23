from uuid import uuid4

from domain import (
    FileInfo,
    OperationContext,
    JobMovedToVerifying,
    JobCompleted,
    ExternalMediaIDs,
)

from application import (
    EventPublisher,
    JobVerifyingProcessManager,
    JobCompletionProcessManager,
    TranscodeVerified,
    TranscodeVerificationFailed,
    TranscodeSuccess,
    EventEnvelope,
)

from tests import (
    FakeFileSystem,
    FakeSyncEventBus,
    FakeRadarrAPIAdapter,
    FakeJellyfinAPIAdapter,
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

def test_JobCompletionProcessManager_emits_TranscodeSuccess_on_success():
    fs = FakeFileSystem()
    bus = FakeSyncEventBus()
    publisher = EventPublisher(bus)
    radarr_api = FakeRadarrAPIAdapter()
    jellyfin_api = FakeJellyfinAPIAdapter()

    transcode_file=FileInfo("/transcode.mp4")
    source_file=FileInfo("/input.mp4")
    media_ids=ExternalMediaIDs.create(6)
    context=OperationContext.create()

    process_manager = JobCompletionProcessManager(event_publisher=publisher,
                                                  radarr_api= radarr_api,
                                                  jellyfin_api=jellyfin_api,
                                                  filesystem=fs)
    
    trigger_event = JobCompleted(job_id=uuid4(),
                                 source_file=source_file,
                                 transcode_file=transcode_file,
                                 media_ids=media_ids,
                                 )
    
    context = OperationContext.create()
    envelope = EventEnvelope.create(event=trigger_event, context=context)

    emitted = []

    def capture(envelope):
        emitted.append(type(envelope.event))

    bus.subscribe(TranscodeSuccess, capture)

    fs.add(source_file.path)
    fs.add(transcode_file.path)
    radarr_api._add_movie(media_identifiers=media_ids, file=source_file, context=context)
    process_manager(envelope)

    assert emitted == [
        TranscodeSuccess,
    ]
