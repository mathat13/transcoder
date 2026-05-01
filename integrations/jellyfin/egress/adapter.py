from domain import (OperationContext)

from integrations import BaseAPIAdapter
from infrastructure.transport.http.models import HTTPRequest
from integrations.jellyfin.egress.requests.headers import JellyfinHeaders

from application import (
    JellyfinLibraryRefreshCapable,
)

class JellyfinAPIAdapter(BaseAPIAdapter,
                         JellyfinLibraryRefreshCapable,):
    service_name = "Jellyfin"

    def __init__(self, client, api_key: str = "fakeapikey", host: str = "jellyfin.local"): 
        base_url = f"http://{host}"
        headers = JellyfinHeaders(authorization=api_key).model_dump(by_alias=True)
        super().__init__(client, base_url, headers)

    def refresh_library(self, context: OperationContext) -> None:
        url_extension = "/Library/Refresh"

        request =  HTTPRequest(
            url=self._generate_url(url_extension),
            headers=self._headers_with_idempotency(context=context),
        )

        response = self.client.post(request)
        self._raise_for_error(response)
