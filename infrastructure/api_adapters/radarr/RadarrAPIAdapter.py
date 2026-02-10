from pydantic import TypeAdapter

from infrastructure.api_adapters.base.BaseAPIAdapter import BaseAPIAdapter
from infrastructure.api_adapters.shared.HTTPRequest import HTTPRequest
from infrastructure.api_adapters.radarr.data_models.headers import RadarrHeaders
from infrastructure.api_adapters.radarr.data_models.get_moviefile import GetMovieFileResponse
from infrastructure.api_adapters.radarr.data_models.rescan_movie import RescanMovieRequest

from domain import (ExternalMediaIDs,
                    FileInfo,
                    OperationContext,
)

from application import (RadarrUpdateMovieFileCapable)

class RadarrAPIAdapter(BaseAPIAdapter,
                       RadarrUpdateMovieFileCapable):
    service_name = "Radarr"

    def __init__(self, client, api_key: str = "fakeapikey", host: str = "radarr.local"): 
        base_url = f"http://{host}/api/v3"
        headers = RadarrHeaders(x_api_key=api_key).model_dump(by_alias=True)
        super().__init__(client, base_url, headers)

    def get_moviefile(self, media_identifiers: ExternalMediaIDs, context: OperationContext) -> FileInfo | None:
        """
        requires: query_params, movie_id, url_extension
        returns: JSON
        """
        
        movie_id = media_identifiers.radarr_movie_id
        query_params = {"movieId": movie_id}
        url_extension = "/moviefile"

        request =  HTTPRequest(
            url=self._generate_url(url_extension),
            headers=self._headers_with_idempotency(context=context),
            query_params=query_params,
        )

        response = self.client.get(request)
        self._raise_for_error(response)

        # Empty response
        if not response.json_data:
            return None
        
        # For non-list-wrapped responses
        #data = GetMovieFileResponse(**response.json_data)

        # For list-wrapped responses
        # Define model to validate against
        model = TypeAdapter(list[GetMovieFileResponse])
        # Validate, while stripping list and assigning to a value for extracting return values
        data = model.validate_python(
            response.json_data
        )[0]

        # Convert to ubiquitous language and pass back to application
        return FileInfo(data.path)

        

    def rescan_movie(self, media_identifiers: ExternalMediaIDs, context: OperationContext) -> None:
        """
        Requires: movie_id, url_extension
        Returns: JSON
        """
        movie_id = media_identifiers.radarr_movie_id
        url_extension = "/command"

        request =  HTTPRequest(
            url=self._generate_url(url_extension),
            headers=self._headers_with_idempotency(context=context),
            data=RescanMovieRequest(movieId=movie_id).model_dump(),
        )

        response = self.client.post(request)
        self._raise_for_error(response)