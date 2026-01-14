from uuid import uuid4

from domain import (
    JobMovedToVerifying,
    FileInfo,
    OperationContext,
)
from application import (
    EventPublisher,
    EventEnvelope,
)

from tests import (
    FakeSyncEventBus
)

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