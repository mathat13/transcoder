from pydantic import TypeAdapter
from uuid import UUID

from infrastructure.api_adapters.base.BaseAPIAdapter import BaseAPIAdapter
from infrastructure.api_adapters.shared.HTTPRequest import HTTPRequest
from infrastructure.api_adapters.radarr.data_models.headers import RadarrHeaders
from infrastructure.api_adapters.radarr.data_models.get_moviefile import GetMovieFileResponse
from infrastructure.api_adapters.radarr.data_models.rescan_movie import RescanMovieRequest

class RadarrAPIAdapter(BaseAPIAdapter):
    service_name = "Radarr"

    def __init__(self, client, api_key: str = "fakeapikey", host: str = "radarr.local"): 
        base_url = f"http://{host}/api/v3"
        headers = RadarrHeaders(x_api_key=api_key).model_dump(by_alias=True)
        super().__init__(client, base_url, headers)

    def get_moviefile(self, movie_id: int, idempotency_key: UUID = None) -> bool:
        if idempotency_key:
            key = idempotency_key
        else:
            key = self._generate_key()
        key = str(key)

        self.headers["idempotency_key"] = key
        
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

    def rescan_movie(self, movie_id: int, idempotency_key: UUID = None) -> None:
        if idempotency_key:
            key = idempotency_key
        else:
            key = self._generate_key()
        key = str(key)

        self.headers["idempotency_key"] = key
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