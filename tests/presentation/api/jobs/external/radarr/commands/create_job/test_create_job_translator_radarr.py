import pytest

from presentation.api.use_cases.jobs.external.radarr.commands.create_job.ingress.translation.translator import CreateJobTranslator
from presentation.api.use_cases.jobs.external.radarr.commands.create_job.ingress.translation.types import IgnoreReason
from presentation.api.use_cases.jobs.external.radarr.commands.create_job.ingress.translation.results import (
    CommandReady,
    Ignored,
    )

from tests.factories.pydantic_factories.radarr_webhook_factory import CreateJobRequestFactory
from application import CreateJobCommand
from domain import (
    FileInfo,
    ExternalMediaIDs,
)

def test_CreateJobTranslator_creates_commandready_successfully():
    # Setup
    source_file = "/data/media.mkv"
    media_id = 1

    # Execution
    result = CreateJobTranslator.translate(
        request=CreateJobRequestFactory(movie__id=media_id,
                                        movieFile__sourceFile=source_file
                                        )
                                        )
    
    # Validation
    assert isinstance(result, CommandReady)

    cmd = result.cmd
    assert isinstance(cmd, CreateJobCommand)
    assert isinstance(cmd.source_file, FileInfo)
    assert str(cmd.source_file.path) == source_file
    assert isinstance(cmd.media_ids, ExternalMediaIDs)
    assert cmd.media_ids.radarr_movie_id == media_id

def test_CreateJobTranslator_creates_ignore_result_correctly():
    # Setup
    source_file = "/data/media.mkv"
    media_id = 1

    # Execution
    result = CreateJobTranslator.translate(
        request=CreateJobRequestFactory(
            movie__id=media_id,
            movieFile__sourceFile=source_file,
            eventType="Unsupported event"
            )
            )
    
    # Validation
    assert isinstance(result, Ignored)

    assert result.reason == IgnoreReason.UNSUPPORTED_EVENT_TYPE