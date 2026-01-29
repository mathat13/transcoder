from abc import ABC, abstractmethod

from uuid import UUID

class ProcessContext(ABC):
    @property
    @abstractmethod
    def operation_id(self) -> UUID:
        ...

    @property
    @abstractmethod
    def payload(self) -> object:
        """Domain data needed by the process (job, media ids, files, etc)."""