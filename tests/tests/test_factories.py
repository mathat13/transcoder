import pytest

from infrastructure import JobModel

def test_job_model_factory(db_session, job_model_factory):
    # Add job_model to database with the create method
    job_model = job_model_factory.create()

    retrieved_job_model = (
        db_session.query(JobModel)
        .filter(JobModel.id == job_model.id)
        .first()
    )

    assert retrieved_job_model is not None
    assert isinstance(retrieved_job_model, JobModel)