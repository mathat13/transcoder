from infrastructure import (
    HTTPResponse,
    HTTPRequest
)

class FakeHTTPClient():

    def __init__(self, response: HTTPResponse):
        self._response = response

    def _send(self, request: HTTPRequest) -> HTTPResponse:
       return self._response
    
    def get(self, request: HTTPRequest) -> HTTPResponse:
        return self._send(request)
    
    def post(self, request: HTTPRequest) -> HTTPResponse:
        return self._send(request)

    def patch(self, request: HTTPRequest) -> HTTPResponse:
        return self._send(request)

    def put(self, request: HTTPRequest) -> HTTPResponse:
        return self._send(request)
    
    def delete(self, request: HTTPRequest) -> HTTPResponse:
        return self._send(request)