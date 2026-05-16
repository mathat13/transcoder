import pytest

from presentation.api.use_cases.jobs.internal.commands.create_job.ingress.request import CreateJobRequest
from presentation.api.use_cases.jobs.internal.commands.create_job.ingress.translation.translator import CreateJobTranslator
from presentation.api.use_cases.jobs.internal.commands.create_job.ingress.translation.results import CommandReady

from application import CreateJobCommand
from domain import FileInfo

def test_ManualCreateJobTranslator_success():
    # Setup
    source_file = "/data/media.mkv"

    # Execution
    result = CreateJobTranslator.translate(request=CreateJobRequest(source_file=source_file))
    
    # Validation
    assert isinstance(result, CommandReady)
    cmd = result.cmd
    assert isinstance(cmd, CreateJobCommand)
    assert isinstance(cmd.source_file, FileInfo)
    assert str(cmd.source_file.path) == source_file