# Observability bounded context

from dataclasses import dataclass
from uuid import UUID, uuid4

@dataclass(frozen=True)
class OperationContext():
    operation_id: UUID

    @classmethod
    def create(cls) -> "OperationContext":
        return cls(
            operation_id=uuid4()
        )