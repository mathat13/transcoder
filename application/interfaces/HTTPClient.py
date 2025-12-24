from typing import Protocol

class HTTPClient(Protocol):
    def get(self) -> None:
        ...
    
    def post(self) -> None:
        ...

    def patch(self) -> None:
        ...

    def delete(self) -> None:
        ...