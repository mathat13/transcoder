from dataclasses import asdict

from infrastructure.api_adapters.shared.HTTPRequest import HTTPRequest
from infrastructure.api_adapters.shared.HTTPResponse import HTTPResponse
from infrastructure.api_adapters.radarr.data_models.test_data_model import (
    DataModelRequestWithParams,
    DataModelRequest,
    DataModelRequestWithParamsValid,
    DataModelRequestValid,
    DataModelResponseValid,
    DataModelResponse,
)

class RadarrAPIAdapter():
    def __init__(self, client):
        self.url = "https://radarr.local/api/v3/movie/1/rescan"
        self.headers = {"X-Api-Key": "fakeapikey"}
        self.client = client

    def validate_data_model(self, data: dict):
        pass

    def generate_request(self) -> HTTPRequest:
        query_params = {"id": 1}
        data_dict = DataModelRequest().__dict__
        validated_data = DataModelRequestValid(**data_dict)
        valid_data = validated_data.model_dump()

        return HTTPRequest(
            url=self.url,
            headers=self.headers,
            query_params=query_params,
            data=valid_data
        )
    
    def generate_request_with_params(self, movie_id: int) -> HTTPRequest:
        query_params = {"id": 1}
        data = DataModelRequestWithParams(movie_id=movie_id).__dict__
        validated_data = DataModelRequestWithParamsValid(**data)
        valid_data = validated_data.model_dump()

        return HTTPRequest(
            url=self.url,
            headers=self.headers,
            query_params=query_params,
            data=valid_data
        )
    
    def retrieve_response(self, request: HTTPRequest) -> HTTPResponse:
        response = self.client.get(request)
        validated_response = DataModelResponseValid(**response.data)
        return response
    
    def return_result(self) -> bool:
        query_params = {"id": 1}
        data=DataModelRequest().__dict__
        validated_data = DataModelRequestValid(**data)
        valid_data = validated_data.model_dump()

        request =  HTTPRequest(
            url=self.url,
            headers=self.headers,
            query_params=query_params,
            data=valid_data
        )

        response = self.client.get(request)

        return bool(response.ok)

    def rescan_movie(self, movie_id: int) -> None:
        pass

    def get_movie(self, movie_id: int) -> None:
        pass