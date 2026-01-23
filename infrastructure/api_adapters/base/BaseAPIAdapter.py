from domain import OperationContext

from application import APIServiceException

from infrastructure.api_adapters.shared.HTTPResponse import HTTPResponse

class BaseAPIAdapter():
    service_name: str

    def __init__(self, client, base_url: str, headers: dict):
        self.client = client
        self.base_url = base_url
        self.headers = headers
    
    def _raise_for_error(self, response: HTTPResponse) -> None:
        if response.ok:
            return

        is_retryable=response.is_server_error

        raise APIServiceException(
            service = self.service_name,
            retryable = is_retryable,
            status_code=response.status_code,
            detail=response.json_data or response.text_data
            )

    def _headers_with_idempotency(self, context: OperationContext) -> dict[str, str]:
        """
        Used so that class header templates are not modified per operation
        """
        idempotency_key = context.operation_id
        headers = dict(self.headers)

        if idempotency_key is not None:
            headers["Idempotency-Key"] = str(idempotency_key)

        return headers
    
    def _generate_url(self, extension: str) -> str:
        return self.base_url + extension