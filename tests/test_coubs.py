import pytest
import requests


def test_get_coub(coub_api, requests_mock, snapshot_factory, coub_permalink):
    requests_mock.get(
        f"/api/v2/coubs/{coub_permalink}",
        json=snapshot_factory(f"api/v2/coubs/{coub_permalink}.json"),
    )

    assert coub_api.coubs.get_coub(coub_permalink)


def test_init_upload(coub_api_auth, requests_mock):
    requests_mock.post(
        "/api/v2/coubs/init_upload", json={"permalink": "1kj8z2", "id": 95_639_280}
    )

    assert coub_api_auth.coubs.init_upload()


def test_upload_video(coub_api_auth, requests_mock, coub_id, tmp_path):
    p = tmp_path / "video.mp4"
    p.write_text("content")
    requests_mock.post(f"/api/v2/coubs/{coub_id}/upload_video", json={"status": "ok"})

    assert coub_api_auth.coubs.upload_video(coub_id, p) == {"status": "ok"}


def test_upload_video__already_upload(coub_api_auth, requests_mock, coub_id, tmp_path):
    p = tmp_path / "video.mp4"
    p.write_text("content")
    requests_mock.post(
        f"/api/v2/coubs/{coub_id}/upload_video",
        json={"error": "wrong_coub_id"},
        status_code=422,
    )

    with pytest.raises(requests.exceptions.HTTPError):
        coub_api_auth.coubs.upload_video(coub_id, p)


def test_upload_audio(coub_api_auth, requests_mock, coub_id, tmp_path):
    p = tmp_path / "audio.mp3"
    p.write_text("content")
    requests_mock.post(f"/api/v2/coubs/{coub_id}/upload_audio", json={"status": "ok"})

    assert coub_api_auth.coubs.upload_audio(coub_id, p) == {"status": "ok"}


def test_upload_audio__already_upload(coub_api_auth, requests_mock, coub_id, tmp_path):
    p = tmp_path / "audio.mp3"
    p.write_text("content")
    requests_mock.post(
        f"/api/v2/coubs/{coub_id}/upload_audio",
        json={"error": "wrong_coub_id"},
        status_code=422,
    )

    with pytest.raises(requests.exceptions.HTTPError):
        coub_api_auth.coubs.upload_audio(coub_id, p)


def test_finalize_upload(coub_api_auth, requests_mock, coub_id):
    requests_mock.post(
        f"/api/v2/coubs/{coub_id}/finalize_upload", json={"status": "ok"}
    )

    assert coub_api_auth.coubs.finalize_upload(
        coub_id, title="Awesome CAT", tags=["cat", "animal"]
    ) == {"status": "ok"}
    assert requests_mock.last_request.qs["sound_enabled"] == ["true"]
    assert requests_mock.last_request.qs["original_visibility_type"] == ["private"]
    assert requests_mock.last_request.qs["tags"] == ["cat,animal"]
    assert requests_mock.last_request.qs["title"] == ["awesome cat"]


def test_finalize_upload__already_finalized(coub_api_auth, requests_mock, coub_id):
    requests_mock.post(
        f"/api/v2/coubs/{coub_id}/finalize_upload",
        json={"error": "wrong_coub_id"},
        status_code=422,
    )
    with pytest.raises(requests.exceptions.HTTPError):
        coub_api_auth.coubs.finalize_upload(
            coub_id, title="Awesome CAT", tags=["cat", "animal"]
        )


def test_get_status(coub_api_auth, requests_mock, coub_id):
    requests_mock.get(
        f"/api/v2/coubs/{coub_id}/finalize_status",
        [
            {"json": {"done": False, "percent_done": 0}},
            {"json": {"done": True, "percent_done": 100}},
        ],
    )

    assert not coub_api_auth.coubs.get_upload_status(coub_id)["done"]
    assert coub_api_auth.coubs.get_upload_status(coub_id)["done"]


def test_get_status__not_found(coub_api_auth, requests_mock):
    requests_mock.get(
        "/api/v2/coubs/1/finalize_status",
        json={"error": "Unhandled exception"},
        status_code=404,
    )

    with pytest.raises(requests.exceptions.HTTPError):
        coub_api_auth.coubs.get_upload_status(1)


def test_edit_coub(coub_api_auth, requests_mock, snapshot_factory, coub_permalink):
    channel_id = 313_669
    requests_mock.post(
        f"/api/v2/coubs/{coub_permalink}/update_info",
        json=snapshot_factory(f"api/v2/coubs/{coub_permalink}.json"),
    )
    assert coub_api_auth.coubs.edit_coub(
        coub_permalink, channel_id, title="Updated Awesome CAT", tags=["run"]
    )
    assert requests_mock.last_request.qs["coub[channel_id]"] == [str(channel_id)]


def test_edit__not_allowed(coub_api_auth, requests_mock):
    coub_permalink = "1gkd7u"
    requests_mock.post(
        f"/api/v2/coubs/{coub_permalink}/update_info",
        json={"error": "You are not allowed to update from this channels"},
        status_code=403,
    )

    with pytest.raises(requests.exceptions.HTTPError):
        assert coub_api_auth.coubs.edit_coub(
            coub_permalink, 123_456, title="Updated Awesome CAT", tags=["run"]
        )
