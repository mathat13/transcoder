from dataclasses import dataclass

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
    headers: dict
    query_params: dict | None = None
    data: dict | None = None

    @property
    def normalized_query_params(self) -> dict:
        return self.query_params or {}

    @property
    def normalized_data(self) -> dict:
        return self.data or {}
