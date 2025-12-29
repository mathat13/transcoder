from typing import Protocol

class HTTPClient(Protocol):
    def get(self, url: str, headers: dict, data: dict) -> dict:
        ...
    
    def post(self, url: str, headers: dict, data: dict) -> dict:
        ...

    def patch(self, url: str, headers: dict, data: dict) -> dict:
        ...

    def delete(self, url: str, headers: dict, data: dict) -> dict:
        ...