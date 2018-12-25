import pytest
import requests


def test_unfollow(coub_api_auth, requests_mock):
    requests_mock.delete("/api/v2/follows", json={"status": "ok"})

    assert coub_api_auth.following.unfollow(4000001, 313000)


def test_ufollow__failed(coub_api_auth, requests_mock):
    requests_mock.delete("/api/v2/follows", json={"status": "fail"}, status_code=422)
    with pytest.raises(requests.exceptions.HTTPError):
        coub_api_auth.following.unfollow(4000001, 313000)


def test_follow(coub_api_auth, requests_mock):
    requests_mock.post("/api/v2/follows", json={"status": "ok"})

    assert coub_api_auth.following.follow(4000001, 313000)


def test_follow__failed(coub_api_auth, requests_mock):
    requests_mock.post("/api/v2/follows", json={"status": "fail"}, status_code=422)
    with pytest.raises(requests.exceptions.HTTPError):
        coub_api_auth.following.follow(4000001, 313000)
