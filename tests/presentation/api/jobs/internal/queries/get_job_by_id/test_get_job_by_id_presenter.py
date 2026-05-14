from tests.factories.JobFactory import JobFactory

from domain import JobStatus

from presentation import GetJobByIDPresenter
from presentation.api.use_cases.jobs.internal.queries.get_job_by_id.egress.responses.success.response import (
    JobNotFoundResponse,
    JobFoundResponse,
)

from application import (
    JobFound,
    JobNotFound
)

def test_GetJobByIDPresenter_with_GetJobByIDJobFound():
    # Setup
    job = JobFactory(status=JobStatus.verifying)
    # Set fake_job_service.verify_job return value
    result = JobFound(job=job)
    
    # Exeution
    response = GetJobByIDPresenter.present(result=result)

    # Validation
    assert isinstance(response, JobFoundResponse)
    assert response.model_dump() == {
        "result": "job_found",
        "data": {
            "id": str(job.id),
            "source_file": str(job.source_file.path),
            "transcode_output_file": str(job.transcode_output_file.path),
            "delivery_file": str(job.delivery_file.path),
            "status": job.status.value
        },
        "meta": None,
    }

def test_GetJobByIDPresenter_with_GetJobByIDNotFound():
    # Setup
    result = JobNotFound()
    
    # Exeution
    response = GetJobByIDPresenter.present(result=result)

    # Validation
    assert isinstance(response, JobNotFoundResponse)
    assert response.model_dump() == {
        "result": "job_not_found",
        "data": {},
        "meta": None,
    }