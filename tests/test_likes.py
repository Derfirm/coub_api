import pytest
import requests


def test_do_like(coub_api_auth, requests_mock):
    requests_mock.post(f"/api/v2/likes", json={"status": "ok"})

    assert coub_api_auth.likes.do_like(93_000_001, 300_001)


def test_do_like__failed(coub_api_auth, requests_mock):
    requests_mock.post(
        f"/api/v2/likes",
        json={
            "status": "fail",
            "errors": "Validation failed",
            "validation_errors": {"channel_id": ["like has already been posted"]},
        },
        status_code=422,
    )

    with pytest.raises(requests.exceptions.HTTPError):
        coub_api_auth.likes.do_like(93_000_001, 300_001)


def test_unlike(coub_api_auth, requests_mock):
    requests_mock.delete(f"/api/v2/likes", json={"status": "ok"})

    assert coub_api_auth.likes.unlike(93_000_001, 300_001)
