class ServiceException(Exception):
    """Base class for failures caused by external services."""

class APIServiceException(ServiceException):
    def __init__(self, service: str, status_code: int, detail: str | dict | None):
        super().__init__(f"{service} API failed with status {status_code}")
        self.service = service
        self.status_code = status_code
        self.detail = detail