from dataclasses import dataclass
from requests.models import Response
from json import JSONDecodeError
from typing import (
    Optional,
    Dict,
    Any,
)

@dataclass(frozen=True)
class HTTPRequest:
    """
    Data class representing an HTTP request.
    Note that headers must be explicitly defined, even if empty.
    Notes:
    GET / DELETE uses:
    - url
    - headers
    - query_params
    - POST / PATCH / PUT uses:
    - url
    - headers
    - query_params
    - data
    """
    url: str
    headers: Dict[str, str]
    query_params: Optional[Dict[str, Any]] = None
    data: Optional[Dict[str, Any]] = None
    timeout: float | None = None

    @property
    def normalized_query_params(self) -> Optional[Dict[str, Any]]:
        return self.query_params or {}

    @property
    def normalized_data(self) -> Optional[Dict[str, Any]]:
        return self.data or {}

@dataclass(frozen=True)
class HTTPResponse:
    ok: bool
    status_code: int
    headers: Dict[str, str]
    url: str
    json_data: Optional[Dict[str, Any]] = None
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