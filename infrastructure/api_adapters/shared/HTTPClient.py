import requests

from infrastructure.api_adapters.shared.HTTPResponse import HTTPResponse

class HTTPClient():
    def __init__(self):
        # Shared state here
        pass

    def get(self, url: str, headers: dict, query_params: dict | None = None) -> HTTPResponse:
        query_params = query_params or {}

        response = requests.get(url, headers=headers, params=query_params)
        return HTTPResponse.from_response(response)
    
    def post(self, url: str, headers: dict, query_params: dict | None = None, data: dict | None = None) -> HTTPResponse:
        query_params = query_params or {}
        data = data or {}

        response = requests.post(url, headers=headers, params=query_params, json=data)
        return HTTPResponse.from_response(response)

    def patch(self, url: str, headers: dict, query_params: dict | None = None, data: dict | None = None) -> HTTPResponse:
        query_params = query_params or {}
        data = data or {}

        response = requests.patch(url, headers=headers, params=query_params, json=data)
        return HTTPResponse.from_response(response)
    
    def put(self, url: str, headers: dict, query_params: dict | None = None, data: dict | None = None) -> HTTPResponse:
        query_params = query_params or {}
        data = data or {}

        response = requests.put(url, headers=headers, params=query_params, json=data)
        return HTTPResponse.from_response(response)

    def delete(self, url: str, headers: dict, query_params: dict | None = None) -> HTTPResponse:
        query_params = query_params or {}

        response = requests.delete(url, headers=headers, params=query_params)
        return HTTPResponse.from_response(response)