import pytest

from tests.factories.JobFactory import JobFactory

from domain import JobStatus

from presentation import DispatchJobPresenter
from presentation.api.use_cases.jobs.internal.commands.dispatch_job.egress.responses.success.response import (
    NoJobAvailableResponse,
    JobDispatchedResponse,
)

from application import (
    NoJobAvailable,
    JobDispatched,
)

def test_DispatchJobResultPresenter_with_JobDispatched():
    # Setup
    job = JobFactory(status=JobStatus.processing)
    result = JobDispatched(
            job=job
            )
    
    # Exeution
    response = DispatchJobPresenter.present(result=result)

    # Validation
    assert isinstance(response, JobDispatchedResponse)
    assert response.model_dump() == {
        "result": "job_dispatched",
        "data": {
            "id": str(job.id),
            "source_file": str(job.source_file.path),
            "transcode_output_file": str(job.transcode_output_file.path),
            },
        "meta": None,
    }

def test_DispatchJobResultPresenter_with_NoJobAvailable():
    # Setup
    result = NoJobAvailable()
    
    # Exeution
    response = DispatchJobPresenter.present(result=result)

    # Validation
    assert isinstance(response, NoJobAvailableResponse)
    assert response.model_dump() == {
        "result": "no_job_available",
        "data": {},
        "meta": None,
    }