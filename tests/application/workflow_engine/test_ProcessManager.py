import pytest

from typing import (Type,
                    List,
)

from tests.bootstrap.bootstrap_test_system import bootstrap_test_system
from tests.fakes.FakeProcessRunner import FakeProcessRunner
from tests.factories.EventFactories import (
    EventEnvelopeFactory,
    JobMovedToVerifyingEventFactory,
    JobCompletedEventFactory,
)
from tests.factories.ExceptionFactories import (
    RetryableExceptionFactory,
    TerminalExceptionFactory,
)

from application import (ProcessRunnerResult,
                         Event,
                         TranscodeVerified,
                         TranscodeVerificationFailed,
                         JobCompletionSuccess,
                         JobCompletionFailure,
                         RetryScheduled,
                         EventEnvelope,
                         )

@pytest.mark.parametrize(
    "result, expected_event_type",
    [
        (ProcessRunnerResult.success(), TranscodeVerified),
        (ProcessRunnerResult.failure(RetryableExceptionFactory()), RetryScheduled),
        (ProcessRunnerResult.failure(TerminalExceptionFactory()), TranscodeVerificationFailed),
    ]
)

def test_process_manager_verification_outcomes(result: ProcessRunnerResult, expected_event_type: Type[Event]):
    system = bootstrap_test_system(runner=FakeProcessRunner(result))
    envelope = EventEnvelopeFactory(event=JobMovedToVerifyingEventFactory())

    handled: List[Event] = []

    def handler(envelope: EventEnvelope) -> None:
        handled.append(envelope.event)
    
    system.publisher.event_bus.subscribe(event_type=expected_event_type, handler=handler)
    
    system.manager.handle(envelope)

    assert isinstance(handled[0], expected_event_type)

@pytest.mark.parametrize(
    "result, expected_event_type",
    [
        (ProcessRunnerResult.success(), JobCompletionSuccess),
        (ProcessRunnerResult.failure(RetryableExceptionFactory()), RetryScheduled),
        (ProcessRunnerResult.failure(TerminalExceptionFactory()), JobCompletionFailure),
    ]
)

def test_process_manager_completion_outcomes(result: ProcessRunnerResult, expected_event_type: Type[Event]):
    system = bootstrap_test_system(runner=FakeProcessRunner(result))
    envelope = EventEnvelopeFactory(event=JobCompletedEventFactory())

    handled: List[Event] = []

    def handler(envelope: EventEnvelope) -> None:
        handled.append(envelope.event)
    
    system.publisher.event_bus.subscribe(event_type=expected_event_type, handler=handler)
    
    system.manager.handle(envelope)

    assert isinstance(handled[0], expected_event_type)






