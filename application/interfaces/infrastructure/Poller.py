from abc import ABC, abstractmethod

class Poller(ABC):
    @abstractmethod
    def poll(self) -> None:
        """Poll outbox and publish ready events."""