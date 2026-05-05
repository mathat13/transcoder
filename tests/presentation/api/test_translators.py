import pytest

from tests.factories.pydantic_factories.radarr_webhook_factory import RadarrWebhookCreateJobRequestFactory

from presentation import (
    ManualCreateJobTranslator,
    ManualCreateRequest,
    CommandReady,
    Ignored,
    IgnoreReason,
    RadarrWebhookCreateJobTranslator,
)

from application import CreateJobCommand

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
    assert isinstance(result, CommandReady)
    cmd = result.command
    assert isinstance(cmd, CreateJobCommand)
    assert isinstance(cmd.source_file, FileInfo)
    assert str(cmd.source_file.path) == source_file

def test_RadarrWebhookCreateJobTranslator_creates_commandready_successfully():
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
    assert isinstance(result, CommandReady)

    cmd = result.command
    assert isinstance(cmd, CreateJobCommand)
    assert isinstance(cmd.source_file, FileInfo)
    assert str(cmd.source_file.path) == source_file
    assert isinstance(cmd.media_ids, ExternalMediaIDs)
    assert cmd.media_ids.radarr_movie_id == media_id

def test_RadarrWebhookCreateJobTranslator_creates_ignore_result_correctly():
    # Setup
    source_file = "/data/media.mkv"
    media_id = 1

    # Execution
    result = RadarrWebhookCreateJobTranslator.translate(
        request=RadarrWebhookCreateJobRequestFactory(movie__id=media_id,
                                                     movieFile__sourceFile=source_file,
                                                     eventType="Unsupported event"
                                                     )
                                                     )
    
    # Validation
    assert isinstance(result, Ignored)

    assert result.reason == IgnoreReason.UNSUPPORTED_EVENT_TYPE

def test_RadarrWebhookCreateJobTranslator_passes_FileInfo_exception_correctly():
    pass

def test_RadarrWebhookCreateJobTranslator_passes_ExternalMediaIDs_exception_correctly():
    pass

def test_ManualCreateJobTranslator_passes_FileInfo_exception_correctly():
    pass