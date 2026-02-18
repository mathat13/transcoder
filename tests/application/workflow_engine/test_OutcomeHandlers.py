import pytest

from tests.bootstrap.TestSystem import TestSystem
from tests.factories.EventFactories import (
    JobCompletedEventFactory,
    EventEnvelopeFactory,
)

from application import (OutcomeHandlerRegistry,
                         ProcessRunnerResult,
                         JobCompletionFailure,
                         JobCompletionSuccess,
                         RetryScheduled,
                         )

def test_OutcomeHandlerRegistry_raises_KeyError_on_no_assembler(test_system: TestSystem):
    registry = OutcomeHandlerRegistry()
    envelope = EventEnvelopeFactory(event=JobCompletedEventFactory())

        # No assembler added to registry

    with pytest.raises(KeyError):
        registry.get(envelope=envelope)

def test_JobCompletionOutcomeHandler_returns_correct_events(test_system: TestSystem):
    def generate_FailedProcessRunnerResult():
        exc = KeyError("Key Error")
        return ProcessRunnerResult.failure(exc=exc)
    
    event = JobCompletedEventFactory()
    envelope = EventEnvelopeFactory(event=event)

    failure_result = generate_FailedProcessRunnerResult()
    success_result = ProcessRunnerResult.success()
    
    handler = test_system.outcome_registry.get(envelope=envelope)

    success = handler.on_success(envelope=envelope, result=success_result)
    failure = handler.on_failure(envelope=envelope, result=failure_result)
    retry = handler.on_retry(envelope=envelope, result=failure_result)

    # Success
    assert isinstance(success, JobCompletionSuccess)
    assert success.job_id == event.job_id

    # Failure
    assert isinstance(failure, JobCompletionFailure)
    assert failure.job_id == event.job_id
    assert failure.reason == failure_result.failure_info.reason

    # Retry
    assert isinstance(retry, RetryScheduled)
    assert retry.original_event == event


