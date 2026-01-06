import requests

from infrastructure.api_adapters.shared.HTTPResponse import HTTPResponse
from infrastructure.api_adapters.shared.HTTPRequest import HTTPRequest


class HTTPClient():
    """
    HTTP Client for making pre-defined HTTP API requests.
    Assumes JSON payloads.
    Expects a HTTPRequest object and returns HTTPResponse object.
    """
    def __init__(self):
        self.default_timeout = 5.0
    
    def get(self, request: HTTPRequest) -> HTTPResponse:
        response = requests.get(request.url,
                                headers=request.headers,
                                params=request.normalized_query_params,
                                timeout=request.timeout or self.default_timeout
                                )
        
        return HTTPResponse.from_response(response)
    
    def post(self, request: HTTPRequest) -> HTTPResponse:
        response = requests.post(request.url,
                                 headers=request.headers,
                                 params=request.normalized_query_params,
                                 json=request.normalized_data,
                                 timeout=request.timeout or self.default_timeout
                                 )
        
        return HTTPResponse.from_response(response)

    def patch(self, request: HTTPRequest) -> HTTPResponse:
        response = requests.patch(request.url,
                                  headers=request.headers,
                                  params=request.normalized_query_params,
                                  json=request.normalized_data,
                                  timeout=request.timeout or self.default_timeout
                                  )
        
        return HTTPResponse.from_response(response)
    
    def put(self, request: HTTPRequest) -> HTTPResponse:
        response = requests.put(request.url,
                                headers=request.headers,
                                params=request.normalized_query_params,
                                json=request.normalized_data,
                                timeout=request.timeout or self.default_timeout
                                )
        
        return HTTPResponse.from_response(response)

    def delete(self, request: HTTPRequest) -> HTTPResponse:
        response = requests.delete(request.url,
                                   headers=request.headers,
                                   params=request.normalized_query_params,
                                   timeout=request.timeout or self.default_timeout
                                   )
        
        return HTTPResponse.from_response(response)