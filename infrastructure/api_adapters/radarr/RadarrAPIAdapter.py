from pydantic import TypeAdapter

from application import APIServiceException

from infrastructure.api_adapters.shared.HTTPRequest import HTTPRequest
from infrastructure.api_adapters.shared.HTTPResponse import HTTPResponse
from infrastructure.api_adapters.radarr.data_models.headers import RadarrHeaders
from infrastructure.api_adapters.radarr.data_models.get_moviefile import GetMovieFileResponse
from infrastructure.api_adapters.radarr.data_models.rescan_movie import RescanMovieRequest

class RadarrAPIAdapter():

    def __init__(self, client, api_key: str = "fakeapikey", host: str = "radarr.local"): 
        self.host = host
        self.base_url = f"http://{host}/api/v3"
        self.headers = RadarrHeaders(x_api_key=api_key).model_dump(by_alias=True)
        self.client = client
    
    def _raise_for_error(self, response: HTTPResponse) -> None:
        if response.ok:
            return

        if response.is_server_error:
            is_retryable=True

        if response.is_client_error:
            is_retryable=False

        raise APIServiceException(
            service = "Radarr",
            retryable = is_retryable,
            status_code=response.status_code,
            detail=response.json_data or response.text_data
            )

    def _generate_url(self, extension: str) -> str:
        return self.base_url + extension

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
        self._raise_for_error(response)
        
        if response.ok:
            # For non-list-wrapped responses
            #GetMovieFileResponse(**response.data)

            # For list-wrapped responses
            TypeAdapter(list[GetMovieFileResponse]).validate_python(
                response.json_data
            )

        return bool(response.ok)

    def rescan_movie(self, movie_id: int) -> None:
        url_extension = "/command"
        url=self._generate_url(url_extension)

        request =  HTTPRequest(
            url=url,
            headers=self.headers,
            data=RescanMovieRequest(movieId=movie_id).model_dump()
        )

        response = self.client.post(request)
        self._raise_for_error(response)
        
        return bool(response.ok)