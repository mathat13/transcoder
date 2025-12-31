import pytest
import requests_mock

from uuid import UUID
from datetime import datetime
from dataclasses import asdict
from pydantic import ValidationError

from domain import (
    Job,
    JobStatus,
    FileInfo
)

from infrastructure import (
    JobMapper,
    JobModel,
    FileSystem,
    HTTPClient,
    HTTPResponse,
    HTTPRequest,
    RadarrAPIAdapter
)

from tests import (
    JobFactory,
    FakeHTTPClient
)

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

def test_JobMapper():
    job = JobFactory()
    job_record = JobMapper.to_JobModel(job)

    assert isinstance(job_record, JobModel)
    assert isinstance(job_record.id, str)
    assert isinstance(job_record.source_path, str)
    assert isinstance(job_record.transcode_path, str)
    assert isinstance(job_record.status, str)
    assert isinstance(job_record.created_at, datetime)
    assert isinstance(job_record.updated_at, datetime)
    assert job_record.source_path == job.source_file.path
    assert job_record.transcode_path == job.transcode_file.path

    converted_job = JobMapper.to_Job(job_record)

    assert isinstance(converted_job, Job)
    assert isinstance(converted_job.id, UUID)
    assert isinstance(converted_job.source_file, FileInfo)
    assert isinstance(converted_job.transcode_file, FileInfo)
    assert isinstance(converted_job.status, JobStatus)
    assert isinstance(converted_job.created_at, datetime)
    assert isinstance(converted_job.updated_at, datetime)
    assert job_record.source_path == converted_job.source_file.path
    assert job_record.transcode_path == converted_job.transcode_file.path

def test_JobRepository_save(db_session, job_repository):
    job = JobFactory()

    job_repository.save(job)

    # Manually retrieve record from db
    retrieved_job = db_session.query(JobModel).filter(JobModel.id == str(job.id)).first()

    # Retrieved job doesn't use JobMapper and so returns a JobModel
    assert retrieved_job.id == str(job.id)

def test_JobRepository_get_job_by_id(db_session, job_repository):
    job = JobFactory()
    job_model = JobMapper.to_JobModel(job)

    db_session.add(job_model)
    db_session.commit()
    db_session.refresh(job_model)

    retrieved_job = job_repository._get_job_by_id(job.id)

    assert isinstance(retrieved_job, Job)
    assert str(retrieved_job.id) == job_model.id

def test_JobRepository_get_next_pending_job(db_session, job_repository, job_model_factory):
    job_model_factory.create_batch(10, status="pending")

    next_job_with_repo = job_repository.get_next_pending_job()
    next_job_direct = (
            db_session.query(JobModel)
            .filter(JobModel.status == "pending")
            .order_by(JobModel.created_at.asc())
            .first()
        )
    
    assert isinstance(next_job_with_repo, Job)
    assert isinstance(next_job_direct, JobModel)
    assert str(next_job_with_repo.id) == next_job_direct.id

def test_JobRepository_get_next_pending_job_no_job_model(db_session, job_repository):
    # Grabbing from empty db
    next_job_with_repo = job_repository.get_next_pending_job()

    next_job_direct = (
            db_session.query(JobModel)
            .filter(JobModel.status == "pending")
            .order_by(JobModel.created_at.asc())
            .first()
        )
    
    assert next_job_direct is None
    assert next_job_with_repo is None

def test_filesystem_exists_returns_true_for_existing_file(tmp_path):
    fs = FileSystem()

    file_path = tmp_path / "output.mp4"
    file_path.write_text("fake data")

    file_info = FileInfo(str(file_path))

    result = fs.exists(file_info)

    # Assert
    assert result is True

def test_filesystem_exists_returns_false_for_non_existing_file(tmp_path):
    fs = FileSystem()

    file_path  = tmp_path / "non_existing.mp4"

    # Don't actually write file

    file_info = FileInfo(str(file_path))

    result = fs.exists(file_info)

    assert result is False

def test_httpclient_get_with_requests_mock():
    client = HTTPClient()
    url = "https://example.com/api/resource"

    with requests_mock.Mocker() as m:
        m.get(
            url,
            json={"message": "hello"},
            status_code=200,
            headers={"Content-Type": "application/json"},
        )

        request = HTTPRequest(
            url=url,
            headers={"Authorization": "Bearer token"},
            query_params={"id": 3},
            )
        
        response = client.get(request)

    assert response.ok is True
    assert response.status_code == 200
    assert response.data == {"message": "hello"}
    assert response.url.startswith(url)

def test_httpclient_post_with_requests_mock():
    client = HTTPClient()
    url = "https://example.com/api/resource"

    with requests_mock.Mocker() as m:
        m.post(
            url,
            json={"message": "hello"},
            status_code=200,
            headers={"Content-Type": "application/json"},
        )

        request = HTTPRequest(
            url=url,
            headers={"Authorization": "Bearer token"},
            data={"key": "value"},
        )

        response = client.post(request)

    assert response.ok is True
    assert response.status_code == 200
    assert response.data == {"message": "hello"}
    assert response.url.startswith(url)

def test_httpclient_put_with_requests_mock():
    client = HTTPClient()
    url = "https://example.com/api/resource"

    with requests_mock.Mocker() as m:
        m.put(
            url,
            json={"message": "hello"},
            status_code=200,
            headers={"Content-Type": "application/json"},
        )

        request = HTTPRequest(
            url=url,
            headers={"Authorization": "Bearer token"},
            data={"key": "value"},
        )
        
        response = client.put(request)

    assert response.ok is True
    assert response.status_code == 200
    assert response.data == {"message": "hello"}
    assert response.url.startswith(url)

def test_httpclient_patch_with_requests_mock():
    client = HTTPClient()
    url = "https://example.com/api/resource"

    with requests_mock.Mocker() as m:
        m.patch(
            url,
            json={"message": "hello"},
            status_code=200,
            headers={"Content-Type": "application/json"},
        )

        request = HTTPRequest(
            url=url,
            headers={"Authorization": "Bearer token"},
            data={"key": "value"},
        )

        response = client.patch(request)

    assert response.ok is True
    assert response.status_code == 200
    assert response.data == {"message": "hello"}
    assert response.url.startswith(url)

def test_httpclient_delete_with_requests_mock():
    client = HTTPClient()
    url = "https://example.com/api/resource"

    with requests_mock.Mocker() as m:
        m.delete(
            url,
            json={"message": "hello"},
            status_code=200,
            headers={"Content-Type": "application/json"},
        )

        request = HTTPRequest(
            url=url,
            headers={"Authorization": "Bearer token"},
            query_params={"id": 3},
        )
        
        response = client.delete(request)

    assert response.ok is True
    assert response.status_code == 200
    assert response.data == {"message": "hello"}
    assert response.url.startswith(url)

def test_RadarrAPIAdapter_generates_valid_HTTPRequest():
    url = "https://radarr.local/api/v3/movie/1/rescan"
    headers = {"X-Api-Key": "fakeapikey"}

    required_request = HTTPRequest(
        url=url,
        headers=headers,
        query_params={"id": 1},
        data={
            "hello": "world"
        }
    )
    response = HTTPResponse(
            ok=True,
            status_code=200,
            headers=headers,
            data={"message": "hello"},
            url=url,
        )
    client = FakeHTTPClient(response=response)
    adapter = RadarrAPIAdapter(client)
    request = adapter.generate_request()

    assert asdict(request) == asdict(required_request)

def test_RadarrAPIAdapter_with_params_generates_valid_HTTPRequest():
    url = "https://radarr.local/api/v3/movie/1/rescan"
    headers = {"X-Api-Key": "fakeapikey"}
    movie_id = 2

    required_request = HTTPRequest(
        url=url,
        headers=headers,
        query_params={"id": 1},
        data={
            "hello": "world",
            "movie_id": movie_id
        }
    )
    response = HTTPResponse(
            ok=True,
            status_code=200,
            headers=headers,
            data={"message": "hello"},
            url=url,
        )
    client = FakeHTTPClient(response=response)
    adapter = RadarrAPIAdapter(client)
    request = adapter.generate_request_with_params(movie_id=movie_id)

    assert asdict(request) == asdict(required_request)


def test_RadarrAPIAdapter_retrieves_correct_HTTPResponse():
    url="https://radarr.local/api/v3/movie/1/rescan"
    headers={"X-Api-Key": "fakeapikey"}

    required_response = HTTPResponse(
            ok=True,
            status_code=200,
            headers=headers,
            data={"message": "hello"},
            url=url,
        )
    
    client = FakeHTTPClient(response=required_response)
    adapter = RadarrAPIAdapter(client)

    request = HTTPRequest(
        url=url,
        headers=headers,
        query_params={"id": 1},
        data={
            "hello": "world"
        }
    )

    response = adapter.retrieve_response(request)

    assert asdict(response) == asdict(required_response)
    assert response is required_response

def test_RadarrAPIAdapter_fails_on_incorrect_data_response():
    url="https://radarr.local/api/v3/movie/1/rescan"
    headers={"X-Api-Key": "fakeapikey"}

    bad_data_response = HTTPResponse(
            ok=True,
            status_code=200,
            headers=headers,
            data={"message": 1},
            url=url,
        )
    
    client = FakeHTTPClient(response=bad_data_response)
    adapter = RadarrAPIAdapter(client)

    request = HTTPRequest(
        url=url,
        headers=headers,
        query_params={"id": 1},
        data={
            "hello": "world"
        }
    )

    pytest.raises(ValidationError, adapter.retrieve_response, request)


def test_RadarrAPIAdapter_returns_True_on_successful_response():
    url="https://radarr.local/api/v3/movie/1/rescan"
    headers={"X-Api-Key": "fakeapikey"}

    success_response = HTTPResponse(
            ok=True,
            status_code=200,
            headers=headers,
            data={"message": "hello"},
            url=url,
        )
    
    client = FakeHTTPClient(response=success_response)
    adapter = RadarrAPIAdapter(client)

    response = adapter.return_result()

    assert response is True

def test_RadarrAPIAdapter_returns_False_on_unsuccessful_response():
    url="https://radarr.local/api/v3/movie/1/rescan"
    headers={"X-Api-Key": "fakeapikey"}

    fail_response = HTTPResponse(
            ok=False,
            status_code=404,
            headers=headers,
            data={"message": "hello"},
            url=url,
        )
    
    client = FakeHTTPClient(response=fail_response)
    adapter = RadarrAPIAdapter(client)

    response = adapter.return_result()

    assert response is False

def test_RadarrAPIAdapter_passes_back_return_values_correctly_when_there_are_multiple():
    pass

def test_Radarr_rescan_movie():
    pass
