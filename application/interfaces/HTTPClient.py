from typing import Protocol

from infrastructure import HTTPResponse

class HTTPClient(Protocol):

    def get(self, url: str, headers: dict, query_params: dict = dict()) -> HTTPResponse:
       ...
    
    def post(self, url: str, headers: dict, query_params: dict = dict(), data: dict = dict()) -> HTTPResponse:
        ...

    def patch(self, url: str, headers: dict, query_params: dict = dict(), data: dict = dict()) -> HTTPResponse:
        ...
    
    def put(self, url: str, headers: dict, query_params: dict = dict(), data: dict = dict()) -> HTTPResponse:
        ...
    
    def delete(self, url: str, headers: dict, query_params: dict = dict()) -> HTTPResponse:
        ...