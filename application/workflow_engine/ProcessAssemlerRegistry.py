from typing import (
    Dict,
    Type,
)

from application.events.EventEnvelope import EventEnvelope
from application.workflow_engine.ProcessRunnerInput import ProcessRunnerInput
from application.interfaces.workflow_engine.ProcessAssembler import ProcessAssembler

from domain import (
    Event,
)

class ProcessAssemblerRegistry:
    # Missing keys raise KeyError
    _by_event: Dict[Type[Event], ProcessAssembler]

    def __init__(self):
        self._by_event = {}

    def register(self, event_type: Type[Event], assembler: ProcessAssembler):
        self._by_event[event_type] = assembler

    def assemble(self, envelope: EventEnvelope) -> ProcessRunnerInput:
        event_type = type(envelope.event)
        try:
            assembler = self._by_event[event_type]
        except KeyError:
            raise KeyError(f"No ProcessAssembler registered for {event_type}")
        return assembler.assemble(envelope)