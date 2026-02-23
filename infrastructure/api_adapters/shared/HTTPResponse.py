from dataclasses import dataclass
from typing import (
    Optional,
    Dict,
)
from requests.models import Response
from json import JSONDecodeError

@dataclass(frozen=True)
class HTTPResponse:
    ok: bool
    status_code: int
    headers: Dict[str, str]
    url: str
    json_data: Optional[Dict[str, str]] = None
    text_data: Optional[str] = None

    @property
    def is_client_error(self) -> bool:
        return 400 <= self.status_code < 500

    @property
    def is_server_error(self) -> bool:
        return self.status_code >= 500

    @classmethod
    def from_response(cls, response: Response) -> "HTTPResponse":
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
        )