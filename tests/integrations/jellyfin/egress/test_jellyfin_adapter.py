import pytest

from domain import OperationContext

from application import APIServiceTerminalException

from infrastructure import HTTPResponse

from integrations import JellyfinAPIAdapter

from tests.fakes.FakeHTTPClient import FakeHTTPClient

def test_JellyfinAPIAdapter_attributes_initialized_correctly():

    client = FakeHTTPClient(response=None)
    adapter = JellyfinAPIAdapter(client, host="jellyfin.local")

    assert adapter.base_url == "http://jellyfin.local"
    assert "MediaBrowser Token=" in adapter.headers["Authorization"]

def test_JellyfinAPIAdapter_refresh_library_returns_true_on_success_with_fake():
    context = OperationContext.create()
    url="http://jellyfin.local"
    response_headers={"X-Api-Key": "fakeapikey"}

    success_response = HTTPResponse(
            ok=True,
            status_code=200,
            headers=response_headers,
            json_data={"message": "success"},
            url=url,
        )
    
    client = FakeHTTPClient(response=success_response)
    adapter = JellyfinAPIAdapter(client)

    adapter.refresh_library(context=context)

def test_JellyfinAPIAdapter_refresh_library_raises_exception_on_failure_with_fake():
    context = OperationContext.create()
    url="http://jellyfin.local"
    response_headers={"X-Api-Key": "fakeapikey"}

    bad_response = HTTPResponse(
            ok=False,
            status_code=402,
            headers=response_headers,
            json_data={"message": "failure"},
            url=url,
        )
    
    client = FakeHTTPClient(response=bad_response)
    adapter = JellyfinAPIAdapter(client)
    
    with pytest.raises(APIServiceTerminalException):
            adapter.refresh_library(context=context)