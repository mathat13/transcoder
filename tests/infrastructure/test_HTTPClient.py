import pytest
import requests_mock
from requests import exceptions

from infrastructure import (
    HTTPClient,
    HTTPRequest,
)

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
    assert response.json_data == {"message": "hello"}
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
    assert response.json_data == {"message": "hello"}
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
    assert response.json_data == {"message": "hello"}
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
    assert response.json_data == {"message": "hello"}
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
    assert response.json_data == {"message": "hello"}
    assert response.url.startswith(url)

def test_client_raises_timeout():
    client = HTTPClient()
    url = "https://example.com/api/resource"

    request = HTTPRequest(
            url=url,
            headers={"Authorization": "Bearer token"},
            data={"key": "value"},
        )

    with requests_mock.Mocker() as m:
        m.get(url, exc=exceptions.Timeout)

        with pytest.raises(exceptions.Timeout):
            client.get(request)


def test_timeout_is_passed_to_requests():
    client = HTTPClient()
    url = "https://example.com/api/resource"

    request = HTTPRequest(
            url=url,
            headers={"Authorization": "Bearer token"},
            data={"key": "value"},
        )

    with requests_mock.Mocker() as m:
        m.get(url, json={"ok": True})

        client.get(request)

        assert m.last_request.timeout == 5.0

        request = HTTPRequest(
            url=url,
            headers={"Authorization": "Bearer token"},
            data={"key": "value"},
            timeout=6
        )

        client.get(request)
        
        assert m.last_request.timeout == 6.0

#def test_retry_then_success():
#    # Create a mock that raises ReadTimeout twice, then returns success
#    responses = [
#        {'exc': exceptions.ReadTimeout},  # 1st call -> timeout
#        {'exc': exceptions.ReadTimeout},  # 2nd call -> timeout
#        {'text': 'OK', 'status_code': 200},        # 3rd call -> success
#    ]
#
#    with requests_mock.Mocker() as m:
#        m.get('https://example.com', response_list=responses)
#
#        call_count = 0
#        for _ in range(3):
#            try:
#                r = requests.get('https://example.com', timeout=1)
#                call_count += 1
#                if r.status_code == 200:
#                    assert r.text == 'OK'
#                    break
#            except exceptions.ReadTimeout:
#                call_count += 1
#
#        assert call_count == 3
