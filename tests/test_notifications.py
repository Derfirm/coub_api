def test_get_list(coub_api_auth, requests_mock, snapshot_factory):
    requests_mock.get(
        "/api/v2/notifications",
        json=snapshot_factory("api/v2/notifications/notifications.json"),
    )

    assert coub_api_auth.notification.get_list()
