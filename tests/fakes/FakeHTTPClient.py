from infrastructure import HTTPResponse

class FakeHTTPClient():

    def __init__(self, response: HTTPResponse):
        self._response = response

    def get(self, url: str, headers: dict, query_params: dict | None = None) -> HTTPResponse:    
       return self._response
    
    def post(self, url: str, headers: dict, query_params: dict | None = None, data: dict | None = None) -> HTTPResponse:
        return self._response

    def patch(self, url: str, headers: dict, query_params: dict | None = None, data: dict | None = None) -> HTTPResponse:
        return self._response
    
    def put(self, url: str, headers: dict, query_params: dict | None = None, data: dict | None = None) -> HTTPResponse:
        return self._response
    
    def delete(self, url: str, headers: dict, query_params: dict | None = None) -> HTTPResponse:
        return self._response