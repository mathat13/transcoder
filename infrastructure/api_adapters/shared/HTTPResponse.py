from dataclasses import dataclass, field
from typing import Optional
import requests.models
from json import JSONDecodeError
from uuid import UUID

@dataclass(frozen=True)
class HTTPResponse:
    ok: bool
    status_code: int
    headers: dict
    url: str
    json_data: Optional[dict] = None
    text_data: Optional[str] = None
    idempotency_key: UUID = None

    @property
    def is_client_error(self) -> bool:
        return 400 <= self.status_code < 500

    @property
    def is_server_error(self) -> bool:
        return self.status_code >= 500

    @classmethod
    def from_response(cls, response: requests.models.Response) -> "HTTPResponse":
        # Cast str key back to UUID
        key = response.request.headers.get("idempotency_key")

        if key:
            key = UUID(key.strip())

        json_data = None
        text_data = None

        content_type = response.headers.get("Content-Type", "").lower()

        if "application/json" in content_type:
            try:
                json_data = response.json()
            except JSONDecodeError:
                json_data = None
        else:
            # .text is always safe
            text_data = response.text or None

        return cls(
            ok=response.ok,
            status_code=response.status_code,
            headers=dict(response.headers),
            json_data=json_data,
            text_data=text_data,
            url=response.url,
            idempotency_key=key
        )