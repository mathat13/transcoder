import pytest

from domain import (
    ExternalMediaIDs,
    FileInfo,
    OperationContext,
)

from application import APIServiceTerminalException

from infrastructure import HTTPResponse

from integrations import RadarrAPIAdapter

from tests.factories.pydantic_factories.radarr_get_moviefile_factory import GetMovieFileResponseFactory
from tests.fakes.FakeHTTPClient import FakeHTTPClient

def test_RadarrAPIAdapter_attributes_initialized_correctly():
    
    client = FakeHTTPClient(response=None)
    adapter = RadarrAPIAdapter(client, host="radarr.local")

    assert adapter.base_url == "http://radarr.local/api/v3"
    assert "fakeapikey" in adapter.headers["X-Api-Key"]

def test_RadarrAPIAdapter_get_moviefile_returns_moviefile_on_hit_with_fake():
    media_identifiers = ExternalMediaIDs(105)
    context = OperationContext.create()
    url="http://radarr.local/api/v3/moviefile"
    response_headers={"X-Api-Key": "fakeapikey"}
    movie_path="/input.mp4"

    success_response = HTTPResponse(
            ok=True,
            status_code=200,
            headers=response_headers,
            json_data=[GetMovieFileResponseFactory(path=movie_path).model_dump()],
            url=url,
        )
    
    client = FakeHTTPClient(response=success_response)
    adapter = RadarrAPIAdapter(client)

    response = adapter.get_moviefile(media_identifiers=media_identifiers, context=context)

    assert isinstance(response, FileInfo)
    assert str(response.path) == movie_path

def test_RadarrAPIAdapter_get_moviefile_returns_None_on_no_hit_with_fake():
    media_identifiers = ExternalMediaIDs(105)
    context = OperationContext.create()
    url="http://radarr.local/api/v3/moviefile"
    response_headers={"X-Api-Key": "fakeapikey"}
    movie_path="/input.mp4"

    response = HTTPResponse(
            ok=True,
            status_code=200,
            headers=response_headers,
            json_data=[],
            url=url,
        )
    
    client = FakeHTTPClient(response=response)
    adapter = RadarrAPIAdapter(client)

    response = adapter.get_moviefile(media_identifiers=media_identifiers, context=context)

    assert response is None

def test_RadarrAPIAdapter_get_moviefile_raises_exception_on_failure_with_fake():
    media_identifiers = ExternalMediaIDs(105)
    context = OperationContext.create()
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
    with pytest.raises(APIServiceTerminalException):
        adapter.get_moviefile(media_identifiers=media_identifiers, context=context)

def test_RadarrAPIAdapter_rescan_movie_returns_true_on_success_with_fake():
    media_identifiers = ExternalMediaIDs(105)
    context = OperationContext.create()
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

    # Will raise exception if not working correctly
    adapter.rescan_movie(media_identifiers=media_identifiers, context=context)

def test_RadarrAPIAdapter_rescan_movie_raises_exception_on_failure_with_fake():
    media_identifiers = ExternalMediaIDs(105)
    context = OperationContext.create()
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
    with pytest.raises(APIServiceTerminalException):
        adapter.rescan_movie(media_identifiers=media_identifiers, context=context)

