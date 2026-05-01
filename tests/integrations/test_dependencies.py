import pytest

from domain import OperationContext

from application import (
    APIServiceRetryableException,
    APIServiceTerminalException,
)

from infrastructure import HTTPResponse

from integrations import BaseAPIAdapter

from tests.fakes.FakeHTTPClient import FakeHTTPClient

def test_BaseAPIAdapter_raise_for_error_raises_correctly():
    url="http://base.local"
    response_headers={"X-Api-Key": "fakeapikey"}

    bad_5xx_response = HTTPResponse(
            ok=False,
            status_code=500,
            headers=response_headers,
            json_data={"message": "failure"},
            url=url,
        )
    
    bad_4xx_response = HTTPResponse(
            ok=False,
            status_code=404,
            headers=response_headers,
            json_data={"message": "failure"},
            url=url,
        )
    
    class TestAPIAdapter(BaseAPIAdapter):
        service_name = "TestService"

    adapter = TestAPIAdapter(client=None, base_url=None, headers=None)

    with pytest.raises(APIServiceRetryableException) as exc:
        adapter._raise_for_error(bad_5xx_response)

    error = exc.value

    assert isinstance(error, APIServiceRetryableException)
    assert error.service == "TestService"
    assert error.detail == {"message": "failure"}
    assert error.status_code == 500

    with pytest.raises(APIServiceTerminalException) as exc:
        adapter._raise_for_error(bad_4xx_response)
    
    error = exc.value
    
    assert isinstance(error, APIServiceTerminalException)
    assert error.service == "TestService"
    assert error.detail == {"message": "failure"}
    assert error.status_code == 404

def test_BaseAPIAdapter_generate_url():
    base_url="http://base.local"
    request_headers={"X-Api-Key": "fakeapikey"}
    
    class TestAPIAdapter(BaseAPIAdapter):
        service_name = "TestService"

    adapter = TestAPIAdapter(client=None, base_url=base_url, headers=None)

    url = adapter._generate_url(extension="/fart")
    
    assert url == "http://base.local/fart"

def test_BaseAPIAdapter_idempotency_key_added_to_headers_correctly():

    class TestAPIAdapter(BaseAPIAdapter):
        service_name = "TestService"

    client = FakeHTTPClient(response=None)
    adapter = TestAPIAdapter(client, base_url=None, headers={"Idempotency-Key": None})
    context = OperationContext.create()

    headers = adapter._headers_with_idempotency(context=context)

    assert headers["Idempotency-Key"] == str(context.operation_id)