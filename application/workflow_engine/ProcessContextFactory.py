from application.workflow_engine.process_contexts.DefaultProcessContext import DefaultProcessContext
from application.workflow_engine.process_contexts.ProcessContext import ProcessContext
from application.events.EventEnvelope import EventEnvelope

class ProcessContextFactory:
    def from_envelope(self, envelope: EventEnvelope) -> ProcessContext:
        return DefaultProcessContext (
            operation_id=envelope.context.operation_id,
            envelope=envelope,
        )