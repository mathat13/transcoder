import pytest
from uuid import UUID

from domain import (
    Job,
    JobStatus,
    JobCreated,
    JobMovedToProcessing,
    JobMovedToVerifying,
    JobCompleted,
    JobFailed,
    FileInfo,
    ExternalMediaIDs,
    OperationContext,
)

from tests import JobFactory

def test_FileInfo_from_string_creation():
    path_str = "/media/source/video.mkv"
    file_info = FileInfo.from_string(path_str)

    assert str(file_info.path) == path_str
    assert isinstance(file_info, FileInfo)

def test_FileInfo_from_parent_and_string_creation():
    path_str = "/media/source/video.mkv"
    from_string_file_info = FileInfo.from_string(path_str)
    from_parent_and_name_file_info = FileInfo.from_parent_and_name(from_string_file_info.parent,
                                                                   from_string_file_info.name)
    
    assert from_parent_and_name_file_info.path == from_string_file_info.path
    assert isinstance(from_parent_and_name_file_info, FileInfo)

def test_OperationContext_factory_create_method():
    context = OperationContext.create()

    assert isinstance(context.operation_id, UUID)

def test_job_added():
    media_ids = ExternalMediaIDs.create(5)
    source_file=FileInfo.from_string("/path/to/source.mkv")
    transcode_output_file=FileInfo.from_string("/path/to/transcode.mkv")
    job = Job.create(source_file=source_file,
                     transcode_output_file=transcode_output_file,
                     media_ids=media_ids)

    assert isinstance(job.id, UUID)
    assert job.status == JobStatus.pending
    assert isinstance(job.external_media_ids, ExternalMediaIDs)
    assert job.source_file is source_file
    assert job.transcode_output_file is transcode_output_file
    assert isinstance(job.delivery_file, FileInfo)
    
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

def test_ExternalMediaIDs_generated_correctly():
    radarr_id = 1
    media_ids = ExternalMediaIDs.create(radarr_id=radarr_id)

    assert media_ids.radarr_movie_id == radarr_id

def test_job_pull_events_works_correctly():
    media_ids = ExternalMediaIDs.create(5)
    source_file=FileInfo.from_string("/path/to/source.mkv")
    job = Job.create(source_file=source_file, media_ids=media_ids)

    assert len(job.events) != 0

    events = job.pull_events()

    assert len(events) != 0
    assert len(job.events) == 0



