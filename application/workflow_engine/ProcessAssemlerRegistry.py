from application.events.EventEnvelope import EventEnvelope
from application.workflow_engine.ProcessRunnerInput import ProcessRunnerInput

class ProcessAssemblerRegistry:
    def __init__(self):
        self._by_event = {}

    def register(self, event_type, assembler):
        self._by_event[event_type] = assembler

    def assemble(self, envelope: EventEnvelope) -> ProcessRunnerInput:
        event_type = type(envelope.event)
        try:
            assembler = self._by_event[event_type]
        except KeyError:
            raise KeyError(f"No ProcessAssembler registered for {event_type}")
        return assembler.assemble(envelope)