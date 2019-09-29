def test_me(coub_api_auth, requests_mock, snapshot_factory):
    requests_mock.get("/api/v2/users/me", json=snapshot_factory("api/v2/users/me.json"))

    assert coub_api_auth.users.me()


def test_change_channel(coub_api_auth, requests_mock, snapshot_factory, mocker):
    channel_id = 123456
    requests_mock.put(
        "/api/v2/users/change_channel",
        json=snapshot_factory("api/v2/users/change_channel.json"),
    )

    response = coub_api_auth.users.change_channel(channel_id)

    assert requests_mock.last_request.qs["channel_id"] == [str(channel_id)]
    assert response == {
        "follows": [],
        "likes": [],
        "recoubs": [],
        "api_token": mocker.ANY,
        "user": {},
        "dislikes": [],
    }
