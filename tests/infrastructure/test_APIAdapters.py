import pytest
from uuid import uuid4

from domain import ExternalMediaIDs

from application import APIServiceException

from infrastructure import (
    HTTPResponse,
    BaseAPIAdapter,
    RadarrAPIAdapter,
    JellyfinAPIAdapter,
)

from tests import (
    GetMovieFileResponseFactory,
    FakeHTTPClient,
)

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

    with pytest.raises(APIServiceException) as exc:
        adapter._raise_for_error(bad_5xx_response)

    error = exc.value

    assert error.retryable == True
    assert error.service == "TestService"
    assert error.detail == {"message": "failure"}
    assert error.status_code == 500

    with pytest.raises(APIServiceException) as exc:
        adapter._raise_for_error(bad_4xx_response)
    
    error = exc.value
    
    assert error.retryable == False
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

def test_RadarrAPIAdapter_attributes_initialized_correctly():
    
    client = FakeHTTPClient(response=None)
    adapter = RadarrAPIAdapter(client, host="radarr.local")

    assert adapter.base_url == "http://radarr.local/api/v3"
    assert "fakeapikey" in adapter.headers["X-Api-Key"]

def test_RadarrAPIAdapter_get_moviefile_returns_true_on_success_with_fake():
    movie_id = ExternalMediaIDs(105)
    idempotency_key = uuid4()
    url="http://radarr.local/api/v3/moviefile"
    response_headers={"X-Api-Key": "fakeapikey"}

    success_response = HTTPResponse(
            ok=True,
            status_code=200,
            headers=response_headers,
            json_data=[GetMovieFileResponseFactory().model_dump()],
            url=url,
        )
    
    client = FakeHTTPClient(response=success_response)
    adapter = RadarrAPIAdapter(client)

    response = adapter.get_moviefile(movie_id=movie_id, idempotency_key=idempotency_key)

    assert response is True

def test_RadarrAPIAdapter_get_moviefile_raises_exception_on_failure_with_fake():
    movie_id = ExternalMediaIDs(105)
    idempotency_key = uuid4()
    url="http://radarr.local/api/v3/moviefile"
    response_headers={"X-Api-Key": "fakeapikey"}

    fail_response = HTTPResponse(
            ok=False,
            status_code=404,
            headers=response_headers,
            json_data={"message": "failure"},
            url=url,
        )
    
    client = FakeHTTPClient(response=fail_response)
    adapter = RadarrAPIAdapter(client)
    with pytest.raises(APIServiceException):
        adapter.get_moviefile(movie_id=movie_id, idempotency_key=idempotency_key)

def test_RadarrAPIAdapter_rescan_movie_returns_true_on_success_with_fake():
    movie_id = ExternalMediaIDs(105)
    idempotency_key = uuid4()
    url="http://radarr.local/api/v3"
    response_headers={"X-Api-Key": "fakeapikey"}

    success_response = HTTPResponse(
            ok=True,
            status_code=200,
            headers=response_headers,
            json_data={"message": "hello"},
            url=url,
        )
    
    client = FakeHTTPClient(response=success_response)
    adapter = RadarrAPIAdapter(client)

    response = adapter.rescan_movie(movie_id=movie_id, idempotency_key=idempotency_key)

    assert response is True

def test_RadarrAPIAdapter_rescan_movie_raises_exception_on_failure_with_fake():
    movie_id = ExternalMediaIDs(105)
    idempotency_key = uuid4()
    url="http://radarr.local/api/v3"
    response_headers={"X-Api-Key": "fakeapikey"}

    fail_response = HTTPResponse(
            ok=False,
            status_code=404,
            headers=response_headers,
            json_data={"message": "failure"},
            url=url,
        )
    
    client = FakeHTTPClient(response=fail_response)
    adapter = RadarrAPIAdapter(client)
    with pytest.raises(APIServiceException):
        adapter.rescan_movie(movie_id=movie_id, idempotency_key=idempotency_key)

def test_JellyfinAPIAdapter_attributes_initialized_correctly():

    client = FakeHTTPClient(response=None)
    adapter = JellyfinAPIAdapter(client, host="jellyfin.local")

    assert adapter.base_url == "http://jellyfin.local"
    assert "MediaBrowser Token=" in adapter.headers["Authorization"]

def test_JellyfinAPIAdapter_refresh_library_returns_true_on_success_with_fake():
    idempotency_key = uuid4()
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

    response = adapter.refresh_library(idempotency_key=idempotency_key)

    assert response is True

def test_JellyfinAPIAdapter_refresh_library_raises_exception_on_failure_with_fake():
    idempotency_key = uuid4()
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
    
    with pytest.raises(APIServiceException):
            adapter.refresh_library(idempotency_key=idempotency_key)

