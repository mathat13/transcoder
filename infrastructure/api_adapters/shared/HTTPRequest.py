from dataclasses import dataclass

@dataclass
class HTTPRequest:
    """
    Data class representing an HTTP request.
    Note that headers must be explicitly defined, even if empty.
    """
    url: str
    headers: dict
    query_params: dict | None = None
    data: dict | None = None
