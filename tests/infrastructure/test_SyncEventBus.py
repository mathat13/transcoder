from uuid import uuid4
from unittest.mock import Mock

from infrastructure import SyncEventBus

from application import (
    EventEnvelope,
)
from domain import (
    JobStatusChanged,
    JobCreated,
    JobMovedToVerifying,
    JobStatus,
    OperationContext,
)

def test_EventBus_calls_subscribers():
    bus = SyncEventBus()

    handled = []

    def handler(envelope):
        handled.append(envelope)

    bus.subscribe(JobStatusChanged, handler)

    event = JobStatusChanged(job_id=uuid4(), old_status=JobStatus.pending, new_status=JobStatus.success)
    context = OperationContext.create()
    envelope = EventEnvelope.create(event, context)

    bus.publish(envelope)

    assert len(handled) == 1
    assert isinstance(handled[0], EventEnvelope)
    assert isinstance(handled[0].event, JobStatusChanged)

def test_EventBus_handler_is_not_called_on_unsubscribed_event():
    bus = SyncEventBus()
    handler = Mock()

    bus.subscribe(JobMovedToVerifying, handler)

    envelope = EventEnvelope.create(
        event=JobCreated(job_id=uuid4(), source_file="file.mkv"),
        context=OperationContext.create(),
    )

    bus.publish(envelope)

    handler.assert_not_called()