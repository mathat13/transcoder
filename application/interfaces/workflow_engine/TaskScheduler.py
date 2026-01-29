from abc import ABC, abstractmethod
from datetime import timedelta

from application.events.EventEnvelope import EventEnvelope

class TaskScheduler(ABC):
    @abstractmethod
    def schedule_retry(
        self,
        event: "EventEnvelope",
        delay: timedelta,
    ) -> None:
        ...