import pytest
import requests


def test_make(coub_api_auth, requests_mock, snapshot_factory):
    requests_mock.post(
        f"/api/v2/recoubs", json=snapshot_factory("api/v2/recoubs/make.json")
    )

    assert coub_api_auth.recoubs.make(93_000_001, 300_001)


def test_make__failed(coub_api_auth, requests_mock):
    requests_mock.post(
        f"/api/v2/recoubs",
        json={"error": "validation failed Validation failed"},
        status_code=422,
    )

    with pytest.raises(requests.exceptions.HTTPError):
        coub_api_auth.recoubs.make(93_000_001, 300_001)


def test_delete_recoub(coub_api_auth, requests_mock):
    requests_mock.delete(f"/api/v2/recoubs", json={"status": "ok"})

    assert coub_api_auth.recoubs.delete(93_000_001, 300_001)


def test_delete_recoub__failed(coub_api_auth, requests_mock):
    requests_mock.delete(
        f"/api/v2/recoubs",
        json={"error": "Couldn't find Coub::Recoub"},
        status_code=404,
    )

    with pytest.raises(requests.exceptions.HTTPError):
        coub_api_auth.recoubs.delete(93_000_001, 300_001)
