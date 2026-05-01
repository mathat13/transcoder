import pytest

from tests.factories.pydantic_factories.radarr_webhook_factory import RadarrWebhookCreateJobRequestFactory

from presentation import (
    ManualCreateJobTranslator,
    ManualCreateRequest,
)

from integrations import RadarrWebhookCreateJobTranslator

from domain import (
    FileInfo,
    ExternalMediaIDs,
)

def test_ManualCreateJobTranslator_success():
    # Setup
    source_file = "/data/media.mkv"

    # Execution
    result = ManualCreateJobTranslator.translate(request=ManualCreateRequest(source_file=source_file))
    
    # Validation
    assert isinstance(result.source_file, FileInfo)
    assert str(result.source_file.path) == source_file

def test_RadarrWebhookCreateJobTranslator_success():
    # Setup
    source_file = "/data/media.mkv"
    media_id = 1

    # Execution
    result = RadarrWebhookCreateJobTranslator.translate(
        request=RadarrWebhookCreateJobRequestFactory(movie__id=media_id,
                                                     movieFile__sourceFile=source_file
                                                     )
                                                     )
    
    # Validation
    assert isinstance(result.source_file, FileInfo)
    assert str(result.source_file.path) == source_file
    assert isinstance(result.media_ids, ExternalMediaIDs)
    assert result.media_ids.radarr_movie_id == media_id
    
def test_ManualCreateJobTranslator_passes_FileInfo_exception_correctly():
    pass

def test_RadarrWebhookCreateJobTranslator_passes_FileInfo_exception_correctly():
    pass

def test_RadarrWebhookCreateJobTranslator_passes_ExternalMediaIDs_exception_correctly():
    pass