from pydantic import TypeAdapter

from infrastructure.api_adapters.shared.HTTPRequest import HTTPRequest
from infrastructure.api_adapters.jellyfin.data_models.headers import JellyfinHeaders

class JellyfinAPIAdapter():

    def __init__(self, client, api_key: str = "fakeapikey", host: str = "jellyfin.local"): 
        self.host = host
        self.base_url = f"http://{host}"
        self.headers = JellyfinHeaders(authorization=api_key).model_dump(by_alias=True)
        self.client = client

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

        return bool(response.ok)
