from pydantic import TypeAdapter

from infrastructure.api_adapters.shared.HTTPRequest import HTTPRequest
from infrastructure.api_adapters.shared.HTTPResponse import HTTPResponse
from infrastructure.api_adapters.radarr.data_models.headers import RadarrHeaders
from infrastructure.api_adapters.radarr.data_models.test_data_model import (
    DataModelRequestWithParams,
    DataModelRequest,
    DataModelResponse,
)
from infrastructure.api_adapters.radarr.data_models.get_moviefile import (
    GetMovieFileResponse
)

class RadarrAPIAdapter():

    def __init__(self, client, api_key: str = "fakeapikey", host: str = "radarr.local"): 
        self.host = host
        self.base_url = f"http://{host}/api/v3"
        self.headers = RadarrHeaders(x_api_key=api_key).model_dump(by_alias=True)
        self.client = client

    def _generate_url(self, extension: str) -> str:
        return self.base_url + extension
    
    def generate_request(self) -> HTTPRequest:
        query_params = {"id": 1}

        # Instantiates and validates the data model
        valid_data = DataModelRequest()

        return HTTPRequest(
            url=self.base_url,
            headers=self.headers,
            query_params=query_params,
            data=valid_data.model_dump()
        )
    
    def generate_request_with_params(self, movie_id: int) -> HTTPRequest:
        query_params = {"id": 1}
        valid_data = DataModelRequestWithParams(movie_id=movie_id)

        return HTTPRequest(
            url=self.base_url,
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
            url=self.base_url,
            headers=self.headers,
            query_params=query_params,
            data=valid_data.model_dump()
        )

        response = self.client.get(request)
        DataModelResponse(**response.data)

        return bool(response.ok)

    def get_moviefile(self, movie_id: int) -> bool:
        query_params = {"movieId": movie_id}
        url_extension = "/moviefile"

        url=self._generate_url(url_extension)

        request =  HTTPRequest(
            url=url,
            headers=self.headers,
            query_params=query_params,
        )

        response = self.client.get(request)
        
        if response.ok:
            # For non-list-wrapped responses
            #GetMovieFileResponse(**response.data)

            # For list-wrapped responses
            TypeAdapter(list[GetMovieFileResponse]).validate_python(
                response.data
            )

        return bool(response.ok)

    def rescan_movie(self, movie_id: int) -> None:
        pass