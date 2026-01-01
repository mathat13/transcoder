from infrastructure.api_adapters.shared.HTTPRequest import HTTPRequest
from infrastructure.api_adapters.shared.HTTPResponse import HTTPResponse
from infrastructure.api_adapters.radarr.data_models.headers import RadarrHeaders
from infrastructure.api_adapters.radarr.data_models.test_data_model import (
    DataModelRequestWithParams,
    DataModelRequest,
    DataModelResponse,
)

class RadarrAPIAdapter():

    def __init__(self, client, api_key: str):
        self.url = "https://radarr.local/api/v3/movie/1/rescan"
        self.headers = RadarrHeaders(X_Api_Key=api_key).model_dump()
        self.client = client

    def generate_request(self) -> HTTPRequest:
        query_params = {"id": 1}
        # Instantiates and validates the data model
        valid_data = DataModelRequest()

        return HTTPRequest(
            url=self.url,
            headers=self.headers,
            query_params=query_params,
            data=valid_data.model_dump()
        )
    
    def generate_request_with_params(self, movie_id: int) -> HTTPRequest:
        query_params = {"id": 1}
        valid_data = DataModelRequestWithParams(movie_id=movie_id)

        return HTTPRequest(
            url=self.url,
            headers=self.headers,
            query_params=query_params,
            data=valid_data.model_dump()
        )
    
    def retrieve_response(self, request: HTTPRequest) -> HTTPResponse:
        response = self.client.get(request)
        # Save to a variable to extract required fields if needed
        DataModelResponse(**response.data) # Validates the response data model
        return response
    
    def return_result(self) -> bool:
        query_params = {"id": 1}
        valid_data = DataModelRequest()

        request =  HTTPRequest(
            url=self.url,
            headers=self.headers,
            query_params=query_params,
            data=valid_data.model_dump()
        )

        response = self.client.get(request)
        DataModelResponse(**response.data)

        return bool(response.ok)

    def rescan_movie(self, movie_id: int) -> None:
        pass

    def get_movie(self, movie_id: int) -> None:
        pass