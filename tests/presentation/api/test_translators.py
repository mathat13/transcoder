import pytest

from presentation import (
    ManualCreateJobTranslator,
    ManualCreateRequest,
)

from domain import (
    FileInfo,
)

def test_ManualCreateJobTranslator_success():
    # Setup
    source_file = "/data/media.mkv"

    # Execution
    result = ManualCreateJobTranslator.translate(request=ManualCreateRequest(source_file=source_file))
    
    # Validation
    assert isinstance(result.source_file, FileInfo)
    assert str(result.source_file.path) == source_file

def test_ManualCreateJobTranslator_passes_FileInfo_exception_correctly():
    pass