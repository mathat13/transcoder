import pytest

from application import APIServiceException

from infrastructure import (
    HTTPResponse,
    RadarrAPIAdapter,
    JellyfinAPIAdapter,
    HTTPClient
)

from tests import (
    GetMovieFileResponseFactory,
    FakeHTTPClient,
)

def test_RadarrAPIAdapter_generate_url():
    client = HTTPClient()
    adapter = RadarrAPIAdapter(client, host="192.168.1.50:7878")

    assert adapter.base_url == "http://192.168.1.50:7878/api/v3"

    url = adapter._generate_url(extension="/fart")
    assert url == "http://192.168.1.50:7878/api/v3/fart"

def test_RadarrAPIAdapter_attributes_initialized_correctly():

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

    assert adapter.base_url == "http://radarr.local/api/v3"
    assert adapter.host == "radarr.local"
    assert "fakeapikey" in adapter.headers["X-Api-Key"]

def test_RadarrAPIAdapter_get_moviefile_returns_true_on_success_with_fake():
    movie_id =105
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

    response = adapter.get_moviefile(movie_id=movie_id)

    assert response is True

def test_RadarrAPIAdapter_get_moviefile_raises_exception_on_failure_with_fake():
    movie_id =105
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
        adapter.get_moviefile(movie_id=movie_id)

def test_RadarrAPIAdapter_rescan_movie_returns_true_on_success_with_fake():
    movie_id =105
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

    response = adapter.rescan_movie(movie_id=movie_id)

    assert response is True

def test_RadarrAPIAdapter_rescan_movie_raises_exception_on_failure_with_fake():
    movie_id =105
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
        adapter.rescan_movie(movie_id=movie_id)

def test_JellyfinAPIAdapter_attributes_initialized_correctly():

    url="http://jellyfin.local/api/v3/moviefile"
    response_headers={"X-Api-Key": "fakeapikey"}

    success_response = HTTPResponse(
            ok=True,
            status_code=200,
            headers=response_headers,
            json_data={"message": "hello"},
            url=url,
        )
    
    client = FakeHTTPClient(response=success_response)
    adapter = JellyfinAPIAdapter(client)

    assert adapter.base_url == "http://jellyfin.local"
    assert adapter.host == "jellyfin.local"
    assert "MediaBrowser Token=" in adapter.headers["Authorization"]

def test_JellyfinAPIAdapter_refresh_library_returns_true_on_success_with_fake():
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

    response = adapter.refresh_library()

    assert response is True

def test_JellyfinAPIAdapter_refresh_library_raises_exception_on_failure_with_fake():
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
            adapter.refresh_library()

