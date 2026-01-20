from pydantic import TypeAdapter
from uuid import UUID

from infrastructure.api_adapters.base.BaseAPIAdapter import BaseAPIAdapter
from infrastructure.api_adapters.shared.HTTPRequest import HTTPRequest
from infrastructure.api_adapters.shared.HTTPResponse import HTTPResponse
from infrastructure.api_adapters.radarr.data_models.headers import RadarrHeaders
from infrastructure.api_adapters.radarr.data_models.get_moviefile import GetMovieFileResponse
from infrastructure.api_adapters.radarr.data_models.rescan_movie import RescanMovieRequest

from domain import ExternalMediaIDs

class RadarrAPIAdapter(BaseAPIAdapter):
    service_name = "Radarr"

    def __init__(self, client, api_key: str = "fakeapikey", host: str = "radarr.local"): 
        base_url = f"http://{host}/api/v3"
        headers = RadarrHeaders(x_api_key=api_key).model_dump(by_alias=True)
        super().__init__(client, base_url, headers)

    def get_moviefile(self, movie_id: ExternalMediaIDs, idempotency_key: UUID) -> bool:
        id = movie_id.radarr_movie_id
        query_params = {"movieId": id}
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

    def rescan_movie(self, movie_id: ExternalMediaIDs, idempotency_key: UUID) -> None:
        id = movie_id.radarr_movie_id
        url_extension = "/command"
        url=self._generate_url(url_extension)

        request =  HTTPRequest(
            url=url,
            headers=self.headers,
            data=RescanMovieRequest(movieId=id).model_dump(),
        )

        response = self.client.post(request)
        self._raise_for_error(response)
        
        return bool(response.ok)