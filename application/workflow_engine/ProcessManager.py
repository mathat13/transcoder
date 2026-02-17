from application.events.EventEnvelope import EventEnvelope
from application.workflow_engine.ProcessAssemlerRegistry import ProcessAssemblerRegistry
from application.workflow_engine.OutcomeHandlerRegistry import OutcomeHandlerRegistry
from application.workflow_engine.ProcessRunner import ProcessRunner
from application.workflow_engine.ProcessStatus import ProcessStatus
from application.events.EventPublisher import EventPublisher
from application.workflow_engine.TaskScheduler import TaskScheduler

class ProcessManager:
    def __init__(self,
                 runner: ProcessRunner,
                 publisher: EventPublisher,
                 assemblers: ProcessAssemblerRegistry,
                 outcomes: OutcomeHandlerRegistry,
                 scheduler: TaskScheduler,
                 ):
        self.runner = runner
        self.publisher = publisher
        self.scheduler = scheduler
        self.assemblers = assemblers
        self.outcomes = outcomes

    def handle(self, envelope: "EventEnvelope") -> None:
        """
        Entry point from event bus.
        Decides whether to run, retry, or abandon a process.
        """
        # Assemble JobRunner payload from envelope
        payload = self.assemblers.assemble(envelope=envelope)

        # Run payload against Runner
        result = self.runner.run(payload=payload)

        # Determine outcome reaction context from envelope
        outcome = self.outcomes.get(envelope=envelope)

        # Decide on reaction
        if result.status == ProcessStatus.SUCCESS:
            # Generate success envelope
            self.publisher.publish(
                event=outcome.on_success(envelope=envelope,
                                   result=result),
                operation_context=envelope.context
            )
        elif result.status == ProcessStatus.FAILURE:
            if result.failure_info.retryable:
                # Generate retry envelope
                self.publisher.publish(
                event=outcome.on_retry(envelope=envelope,
                                   result=result),
                operation_context=envelope.context
            )
            else:
                # Generate terminal failure envelope
                self.publisher.publish(
                event=outcome.on_failure(envelope=envelope,
                                   result=result),
                operation_context=envelope.context
            )
            
            