import pytest

from domain import (
    ExternalMediaIDs,
    OperationContext,
    FileInfo,
)
from tests import (
    FakeRadarrAPIAdapter,
    FakeJellyfinAPIAdapter,
)


def test_FakeRadarrAPIAdapter_add_movie_works_correctly():
    adapter = FakeRadarrAPIAdapter()

    media_identifiers = ExternalMediaIDs.create(105)
    file = FileInfo("/test/path.mkv")
    context = OperationContext.create()

    adapter._add_movie(media_identifiers, file, context)

    assert adapter.moviefiles[media_identifiers.radarr_movie_id] == file

def test_FakeRadarrAPIAdapter_get_movieFile():
    adapter = FakeRadarrAPIAdapter()

    media_identifiers = ExternalMediaIDs.create(105)
    file = FileInfo("/test/path.mkv")
    context = OperationContext.create()

    adapter._add_movie(media_identifiers, file, context)

    response = adapter.get_moviefile(media_identifiers, context)

    assert response == file
    assert response is file    

def test_FakeRadarrAPIAdapter_rescan_movie():
    adapter = FakeRadarrAPIAdapter()

    media_identifiers = ExternalMediaIDs.create(105)
    file = FileInfo("/test/path.mkv")
    context = OperationContext.create()

    adapter._add_movie(media_identifiers, file, context)

    adapter.rescan_movie(media_identifiers, context)

    assert adapter.rescan_called_with[0] == media_identifiers.radarr_movie_id

def test_FakeJellyfinAPIAdapter_refresh_library():
    adapter = FakeJellyfinAPIAdapter()

    context = OperationContext.create()

    adapter.refresh_library(context)

    assert adapter.refresh_library_call_count == 1

    adapter.refresh_library(context)

    assert adapter.refresh_library_call_count == 2

    for i in range(0, 9):
        adapter.refresh_library(context)

    assert adapter.refresh_library_call_count == 11
