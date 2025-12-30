from infrastructure import HTTPResponse

class HTTPClient():

    def get(self, url: str, headers: dict, query_params: dict | None = None) -> HTTPResponse:
       ...
    
    def post(self, url: str, headers: dict, query_params: dict | None = None, data: dict | None = None) -> HTTPResponse:
        ...

    def patch(self, url: str, headers: dict, query_params: dict | None = None, data: dict | None = None) -> HTTPResponse:
        ...
    
    def put(self, url: str, headers: dict, query_params: dict | None = None, data: dict | None = None) -> HTTPResponse:
        ...
    
    def delete(self, url: str, headers: dict, query_params: dict | None = None) -> HTTPResponse:
        ...