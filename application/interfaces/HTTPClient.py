from typing import Protocol

from infrastructure import (
    HTTPResponse,
    HTTPRequest
)

class HTTPClient(Protocol):
    """
    HTTP Client for making pre-defined HTTP requests.
    Expects HTTPRequest object and returns HTTPResponse object.
    """
    def get(self, request: HTTPRequest) -> HTTPResponse:
        ...
    
    def post(self, request: HTTPRequest) -> HTTPResponse:
        ...

    def patch(self, request: HTTPRequest) -> HTTPResponse:
        ...
    
    def put(self, request: HTTPRequest) -> HTTPResponse:
        ...

    def delete(self, request: HTTPRequest) -> HTTPResponse:
        ...