from tests.factories.EventFactories import (
    JobMovedToVerifyingEventFactory,
    JobCompletedEventFactory,
    JobMovedToProcessingEventFactory,
)
from tests.bootstrap.Types import JobServiceTestSystem

from domain import (
    JobMovedToVerifying,
    OperationContext,
)
from application import (
    EventEnvelope,
)

def test_EventPublisher_generates_envelope_correctly(job_service_test_system: JobServiceTestSystem):
    domain_event = JobMovedToVerifyingEventFactory()
    context = OperationContext.create()
    envelope = job_service_test_system.publisher.create_envelope(domain_event, context)

    assert envelope.context == context
    assert isinstance(envelope.event, type(domain_event))
    assert envelope.context is context
    assert isinstance(envelope, EventEnvelope)

def test_EventPublisher_publish_publishes_correctly(job_service_test_system: JobServiceTestSystem):
    
    #Setup
    domain_event = JobMovedToVerifyingEventFactory()
    context = OperationContext.create()

    # Execution
    job_service_test_system.publisher.publish(domain_event, context)

    assert len(job_service_test_system.event_bus.processed_envelopes_of_type(event_type=JobMovedToVerifying)) == 1

def test_EventPublisher_publishes_OperationContext_consistently(job_service_test_system: JobServiceTestSystem):
    
    # Setup
    events = [
        JobMovedToVerifyingEventFactory(),
        JobMovedToVerifyingEventFactory(),
        JobCompletedEventFactory(),
        JobMovedToProcessingEventFactory(),
        JobMovedToProcessingEventFactory(),
    ]
    context = OperationContext.create()

    # Execution
    job_service_test_system.publisher.publish_all(events=events, operation_context=context)

    envelopes = job_service_test_system.event_bus.processed_envelopes_of_type(event_type=None)
    for envelope in envelopes:
        assert envelope.context == context
