import pytest

from tests.bootstrap.TestSystem import TestSystem
from tests.factories.EventFactories import (
    JobCompletedEventFactory,
    JobMovedToVerifyingEventFactory,
    EventEnvelopeFactory,
)
from tests.factories.ExceptionFactories import (
    RetryableExceptionFactory,
    TerminalExceptionFactory,
)

from application import (OutcomeHandlerRegistry,
                         ProcessRunnerResult,
                         JobCompletionFailure,
                         JobCompletionSuccess,
                         TranscodeVerified,
                         TranscodeVerificationFailed,
                         RetryScheduled,
                         JobVerificationOutcomeHandler,
                         JobCompletionOutcomeHandler,
                         )

def test_OutcomeHandlerRegistry_raises_KeyError_on_no_assembler():
    registry = OutcomeHandlerRegistry()
    envelope = EventEnvelopeFactory(event=JobCompletedEventFactory())

        # No assembler added to registry

    with pytest.raises(KeyError):
        registry.get(envelope=envelope)

def test_JobCompletionOutcomeHandler_returns_correct_events(test_system: TestSystem):
    
    envelope = EventEnvelopeFactory(event=JobCompletedEventFactory())
    
    handler = test_system.outcome_registry.get(envelope=envelope)
    assert isinstance(handler, JobCompletionOutcomeHandler)

    success_result = ProcessRunnerResult.success()
    failure_result = ProcessRunnerResult.failure(TerminalExceptionFactory())
    retry_result = ProcessRunnerResult.failure(RetryableExceptionFactory())

    success_outcome = handler.on_success(envelope=envelope, result=success_result)
    failure_outcome = handler.on_failure(envelope=envelope, result=failure_result)
    retry_outcome = handler.on_retry(envelope=envelope, result=retry_result)

    assert isinstance(success_outcome, JobCompletionSuccess)
    assert isinstance(failure_outcome, JobCompletionFailure)
    assert isinstance(retry_outcome, RetryScheduled)

def test_JobVerificationOutcomeHandler_returns_correct_events(test_system: TestSystem):
    
    envelope = EventEnvelopeFactory(event=JobMovedToVerifyingEventFactory())
    
    handler = test_system.outcome_registry.get(envelope=envelope)
    assert isinstance(handler, JobVerificationOutcomeHandler)

    success_result = ProcessRunnerResult.success()
    failure_result = ProcessRunnerResult.failure(TerminalExceptionFactory())
    retry_result = ProcessRunnerResult.failure(RetryableExceptionFactory())

    success_outcome = handler.on_success(envelope=envelope, result=success_result)
    failure_outcome = handler.on_failure(envelope=envelope, result=failure_result)
    retry_outcome = handler.on_retry(envelope=envelope, result=retry_result)

    assert isinstance(success_outcome, TranscodeVerified)
    assert isinstance(failure_outcome, TranscodeVerificationFailed)
    assert isinstance(retry_outcome, RetryScheduled)


