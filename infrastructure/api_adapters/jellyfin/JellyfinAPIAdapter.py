from application import APIServiceException

from infrastructure.api_adapters.shared.HTTPRequest import HTTPRequest
from infrastructure.api_adapters.shared.HTTPResponse import HTTPResponse
from infrastructure.api_adapters.jellyfin.data_models.headers import JellyfinHeaders

class JellyfinAPIAdapter():

    def __init__(self, client, api_key: str = "fakeapikey", host: str = "jellyfin.local"): 
        self.host = host
        self.base_url = f"http://{host}"
        self.headers = JellyfinHeaders(authorization=api_key).model_dump(by_alias=True)
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

    def refresh_library(self) -> bool:
        url_extension = "/Library/Refresh"
        url=self._generate_url(url_extension)

        request =  HTTPRequest(
            url=url,
            headers=self.headers,
        )

        response = self.client.post(request)
        self._raise_for_error(response)

        return bool(response.ok)
