from pydantic import TypeAdapter
from uuid import UUID

from infrastructure.api_adapters.base.BaseAPIAdapter import BaseAPIAdapter
from infrastructure.api_adapters.shared.HTTPRequest import HTTPRequest
from infrastructure.api_adapters.shared.HTTPResponse import HTTPResponse
from infrastructure.api_adapters.radarr.data_models.headers import RadarrHeaders
from infrastructure.api_adapters.radarr.data_models.get_moviefile import GetMovieFileResponse
from infrastructure.api_adapters.radarr.data_models.rescan_movie import RescanMovieRequest

from domain import (ExternalMediaIDs,
                    FileInfo,
)

class RadarrAPIAdapter(BaseAPIAdapter):
    service_name = "Radarr"

    def __init__(self, client, api_key: str = "fakeapikey", host: str = "radarr.local"): 
        base_url = f"http://{host}/api/v3"
        headers = RadarrHeaders(x_api_key=api_key).model_dump(by_alias=True)
        super().__init__(client, base_url, headers)

    def get_moviefile(self, media_identifier: ExternalMediaIDs, idempotency_key: UUID) -> FileInfo | None:
        movie_id = media_identifier.radarr_movie_id
        query_params = {"movieId": movie_id}
        url_extension = "/moviefile"

        request =  HTTPRequest(
            url=self._generate_url(url_extension),
            headers=self._headers_with_idempotency(idempotency_key=idempotency_key),
            query_params=query_params,
        )

        response = self.client.get(request)
        self._raise_for_error(response)
        
        # For non-list-wrapped responses
        #data = GetMovieFileResponse(**response.data)

        # For list-wrapped responses
        # Define model to validate against
        model = TypeAdapter(list[GetMovieFileResponse])
        # Validate, while stripping list and assigning to a value for extracting return values
        data = model.validate_python(
            response.json_data
        )[0]

        return FileInfo(data.path)

        

    def rescan_movie(self, media_identifier: ExternalMediaIDs, idempotency_key: UUID) -> None:
        movie_id = media_identifier.radarr_movie_id
        url_extension = "/command"

        request =  HTTPRequest(
            url=self._generate_url(url_extension),
            headers=self._headers_with_idempotency(idempotency_key=idempotency_key),
            data=RescanMovieRequest(movieId=movie_id).model_dump(),
        )

        response = self.client.post(request)
        self._raise_for_error(response)
        
        return bool(response.ok)