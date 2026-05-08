from presentation import (
    JobSummaryMapper,
    JobSummaryDTO,
)

from tests.factories.JobFactory import JobFactory

def test_JobSummaryMapper_provides_correct_JobSummaryDTO():
    job = JobFactory()

    summarydto = JobSummaryMapper.to_job_summary(job=job)

    assert isinstance(summarydto, JobSummaryDTO)
    assert isinstance(summarydto.id, str)
    assert isinstance(summarydto.source_file, str)
    assert isinstance(summarydto.transcode_output_file, str)
    assert isinstance(summarydto.delivery_file, str)
    assert isinstance(summarydto.status, str)
    assert summarydto.source_file == str(job.source_file.path)
    assert summarydto.transcode_output_file == str(job.transcode_output_file.path)
    assert summarydto.delivery_file == str(job.delivery_file.path)
    assert summarydto.status == job.status.value
