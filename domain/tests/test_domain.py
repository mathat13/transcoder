import pytest

from domain import Job, JobStatus, JobFactory

def test_job_added():
    job = Job.create(job_id=1,job_type="episode", source_path="/path/to/source.mkv")
    assert job.id is not None
    assert job.status == JobStatus.pending
    assert isinstance(job, Job)

def test_job_transitions_from_pending_to_processing():
    job = JobFactory(status=JobStatus.pending)
    job.transition_to(JobStatus.processing)
    assert job.status == JobStatus.processing
    assert len(job.events) == 1
    event = job.events[0]
    assert event.old_status == JobStatus.pending.value
    assert event.new_status == JobStatus.processing.value

def test_job_transitions_from_processing_to_verifying():
    job = JobFactory(status=JobStatus.processing)
    job.transition_to(JobStatus.verifying)
    assert job.status == JobStatus.verifying
    assert len(job.events) == 1
    event = job.events[0]
    assert event.old_status == JobStatus.processing.value
    assert event.new_status == JobStatus.verifying.value

def test_job_transitions_from_processing_to_error():
    job = JobFactory(status=JobStatus.processing)
    job.transition_to(JobStatus.error)
    assert job.status == JobStatus.error
    assert len(job.events) == 1
    event = job.events[0]
    assert event.old_status == JobStatus.processing.value
    assert event.new_status == JobStatus.error.value

def test_job_transitions_from_verifying_to_success():
    job = JobFactory(status=JobStatus.verifying)
    job.transition_to(JobStatus.success)
    assert job.status == JobStatus.success
    assert len(job.events) == 1
    event = job.events[0]
    assert event.old_status == JobStatus.verifying.value
    assert event.new_status == JobStatus.success.value

def test_job_transitions_from_verifying_to_error():
    job = JobFactory(status=JobStatus.verifying)
    job.transition_to(JobStatus.error)
    assert job.status == JobStatus.error
    assert len(job.events) == 1
    event = job.events[0]
    assert event.old_status == JobStatus.verifying.value
    assert event.new_status == JobStatus.error.value

def test_invalid_transition_raises_value_error():
    job = JobFactory(status=JobStatus.pending)
    with pytest.raises(ValueError) as excinfo:
        job.transition_to(JobStatus.success)
    assert "Invalid transition" in str(excinfo.value)




