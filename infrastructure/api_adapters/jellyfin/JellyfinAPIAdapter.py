from uuid import UUID

from infrastructure.api_adapters.base.BaseAPIAdapter import BaseAPIAdapter
from infrastructure.api_adapters.shared.HTTPRequest import HTTPRequest
from infrastructure.api_adapters.jellyfin.data_models.headers import JellyfinHeaders

class JellyfinAPIAdapter(BaseAPIAdapter):
    service_name = "Jellyfin"

    def __init__(self, client, api_key: str = "fakeapikey", host: str = "jellyfin.local"): 
        base_url = f"http://{host}"
        headers = JellyfinHeaders(authorization=api_key).model_dump(by_alias=True)
        super().__init__(client, base_url, headers)

    def refresh_library(self, idempotency_key: UUID = None) -> bool:
        if idempotency_key:
            key = idempotency_key
        else:
            key = self._generate_key()
        key = str(key)

        self.headers["idempotency_key"] = key
        url_extension = "/Library/Refresh"
        url=self._generate_url(url_extension)

        request =  HTTPRequest(
            url=url,
            headers=self.headers,
        )

        response = self.client.post(request)
        self._raise_for_error(response)

        return bool(response.ok)
