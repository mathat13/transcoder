from typing import (
    TypeVar,
    Iterable,
)

from abc import ABC, abstractmethod

from domain import (
    Event,
    OperationContext,
)

from application import EventEnvelope

E = TypeVar("E", bound=Event)

class EventPublisher(ABC):
    @abstractmethod
    def create_envelope(self, event: Event, operation_context: OperationContext) -> EventEnvelope:
        pass

    @abstractmethod
    def publish(self, event: Event, operation_context: OperationContext) -> None:
        pass

    @abstractmethod
    def publish_all(self, events: Iterable[Event], operation_context: OperationContext) -> None:
        pass