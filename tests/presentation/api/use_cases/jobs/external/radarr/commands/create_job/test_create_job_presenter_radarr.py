import pytest

from tests.factories.JobFactory import JobFactory

from domain import JobStatus

from presentation.api.use_cases.jobs.external.radarr.commands.create_job.egress.presenter import CreateJobPresenter
from presentation.api.use_cases.jobs.external.radarr.commands.create_job.egress.responses.success.response import JobCreatedResponse

from application.services.jobs.commands.create_job.results import JobCreated as JobCreatedResult

def test_CreateJobResultPresenter_with_JobCreatedResult():
    # Setup
    job = JobFactory(status=JobStatus.pending)
    result = JobCreatedResult(
            job=job
            )
    
    # Exeution
    response = CreateJobPresenter.present(result=result)

    # Validation
    assert isinstance(response, JobCreatedResponse)
    assert response.model_dump() == {
        "result": "job_created",
        "data": {
            "id": str(job.id),
            "status": job.status.value,
            "source_file": str(job.source_file.path)
        },
        "meta": {},
    }