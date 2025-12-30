import requests

from infrastructure.api_adapters.shared.HTTPResponse import HTTPResponse
from infrastructure.api_adapters.shared.HTTPRequest import HTTPRequest


class HTTPClient():
    """
    HTTP Client for making pre-defined HTTP requests.
    Expects HTTPRequest object and returns HTTPResponse object.
    Expects headers to be defined if empty
    """
    def __init__(self):
        # Shared state here
        pass
    
    def get(self, request: HTTPRequest) -> HTTPResponse:
        query_params = request.query_params or {}

        response = requests.get(request.url, headers=request.headers, params=query_params)
        return HTTPResponse.from_response(response)
    
    def post(self, request: HTTPRequest) -> HTTPResponse:
        query_params = request.query_params or {}
        data = request.data or {}

        response = requests.post(request.url, headers=request.headers, params=query_params, json=data)
        return HTTPResponse.from_response(response)

    def patch(self, request: HTTPRequest) -> HTTPResponse:
        query_params = request.query_params or {}
        data = request.data or {}

        response = requests.patch(request.url, headers=request.headers, params=query_params, json=data)
        return HTTPResponse.from_response(response)
    
    def put(self, request: HTTPRequest) -> HTTPResponse:
        query_params = request.query_params or {}
        data = request.data or {}

        response = requests.put(request.url, headers=request.headers, params=query_params, json=data)
        return HTTPResponse.from_response(response)

    def delete(self, request: HTTPRequest) -> HTTPResponse:
        query_params = request.query_params or {}

        response = requests.delete(request.url, headers=request.headers, params=query_params)
        return HTTPResponse.from_response(response)