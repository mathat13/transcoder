import pytest

from domain import (
    Job,
    JobStatus,
    JobFactory,
    JobCreated,
    JobMovedToProcessing,
    JobMovedToVerifying,
    JobCompleted,
    JobFailed,
    FileInfo
) 

def test_FileInfo_creation():
    path_str = "/media/source/video.mkv"
    file_info = FileInfo(path_str)

    assert file_info.path == path_str
    assert isinstance(file_info, FileInfo)

    transcoded = file_info.transcoded_path

    assert isinstance(transcoded, FileInfo)
    assert transcoded.path == "/media/source/video_transcoded.mkv"

def test_FileInfo_invalid_path_raises_value_error():

    # String without a slash
    with pytest.raises(ValueError) as excinfo:
        FileInfo("invalidpath")
    assert "Invalid file path format." in str(excinfo.value)

    # Empty string
    with pytest.raises(ValueError) as excinfo:
        FileInfo("")
    assert "Invalid file path format." in str(excinfo.value)



def test_job_added():
    job = Job.create(job_type="episode", source_path="/path/to/source.mkv")

    assert job.id is not None
    assert job.status == JobStatus.pending
    assert isinstance(job.source_path, FileInfo)
    assert job.source_path.path == "/path/to/source.mkv"
    assert isinstance(job.output_path, FileInfo)
    assert job.output_path.path == "/path/to/source_transcoded.mkv"
    
    assert len(job.events) == 1
    event = job.events[0]
    assert isinstance(event, JobCreated)

def test_job_transitions_from_pending_to_processing():
    job = JobFactory(status=JobStatus.pending)
    job.transition_to(JobStatus.processing)
    assert job.status == JobStatus.processing    
    
    assert len(job.events) == 1
    event = job.events[0]
    assert isinstance(event, JobMovedToProcessing)

def test_job_transitions_from_processing_to_verifying():
    job = JobFactory(status=JobStatus.processing)
    job.transition_to(JobStatus.verifying)
    assert job.status == JobStatus.verifying
    
    assert len(job.events) == 1
    event = job.events[0]
    assert isinstance(event, JobMovedToVerifying)

def test_job_transitions_from_processing_to_error():
    job = JobFactory(status=JobStatus.processing)
    job.transition_to(JobStatus.error)
    assert job.status == JobStatus.error
    
    assert len(job.events) == 1
    event = job.events[0]
    assert isinstance(event, JobFailed)

def test_job_transitions_from_verifying_to_success():
    job = JobFactory(status=JobStatus.verifying)
    job.transition_to(JobStatus.success)
    assert job.status == JobStatus.success
    
    assert len(job.events) == 1
    event = job.events[0]
    assert isinstance(event, JobCompleted)

def test_job_transitions_from_verifying_to_error():
    job = JobFactory(status=JobStatus.verifying)
    job.transition_to(JobStatus.error)
    assert job.status == JobStatus.error
    
    assert len(job.events) == 1
    event = job.events[0]
    assert isinstance(event, JobFailed)

def test_invalid_transition_raises_value_error():
    job = JobFactory(status=JobStatus.pending)
    with pytest.raises(ValueError) as excinfo:
        job.transition_to(JobStatus.success)
    assert "Invalid transition" in str(excinfo.value)
