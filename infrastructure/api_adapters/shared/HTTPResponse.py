from dataclasses import dataclass
import requests.models

@dataclass(frozen=True)
class HTTPResponse:
    ok: bool
    status_code: int
    headers: dict
    data: dict
    url: str

    @classmethod
    def from_response(cls, response: requests.models.Response) -> "HTTPResponse":
        return cls(
            ok=response.ok,
            status_code=response.status_code,
            headers=response.headers,
            data=response.json(),
            url=response.url
        )