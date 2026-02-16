from datetime import timedelta

from application.events.EventEnvelope import EventEnvelope

class TaskScheduler():
    def schedule_retry(
        self,
        event: "EventEnvelope",
        delay: timedelta,
    ) -> None:
        pass