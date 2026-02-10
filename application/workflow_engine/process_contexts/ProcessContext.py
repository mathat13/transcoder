from dataclasses import dataclass

from application import (
      EventEnvelope,
)

from domain import (
    OperationContext,
)

@dataclass(frozen=True)
class ProcessContext:
    operation_context: OperationContext
    envelope: EventEnvelope