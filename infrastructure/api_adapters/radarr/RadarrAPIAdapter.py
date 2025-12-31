from infrastructure.api_adapters.shared.HTTPRequest import HTTPRequest
from infrastructure.api_adapters.shared.HTTPResponse import HTTPResponse

class RadarrAPIAdapter():
    def __init__(self, client):
        self.url = "https://radarr.local/api/v3/movie/1/rescan"
        self.client = client

    def generate_request(self) -> HTTPRequest:
        return HTTPRequest(
            url=self.url,
            headers={"X-Api-Key": "fakeapikey"},
            query_params={"id": 1},
            data={
                "hello": "world"
            }
        )
    
    def retrieve_response(self, request: HTTPRequest) -> HTTPResponse:
        response = self.client.get(request)
        return response
    
    def return_result(self) -> bool:
        request = HTTPRequest(
            url=self.url,
            headers={"X-Api-Key": "fakeapikey"},
            query_params={"id": 1},
            data={
                "hello": "world"
            }
        )

        response = self.client.get(request)
        return bool(response.ok)

    def rescan_movie(self, movie_id: int) -> None:
        pass

    def get_movie(self, movie_id: int) -> None:
        pass