def test_get_friend_data(coub_api_auth, requests_mock, snapshot_factory):
    requests_mock.get(
        f"/api/v2/friends", json=snapshot_factory(f"api/v2/friends/get_data.json")
    )

    assert coub_api_auth.friends.get_data()


def test_get_friend_data_from_provider(coub_api_auth, requests_mock, snapshot_factory):
    requests_mock.get(
        f"/api/v2/friends",
        json=snapshot_factory(f"api/v2/friends/get_data_google.json"),
    )

    assert coub_api_auth.friends.get_data(provider="google")


def test_get_friend_recommended(coub_api_auth, requests_mock, snapshot_factory):
    requests_mock.get(
        f"/api/v2/friends/recommended",
        json=snapshot_factory(f"api/v2/friends/recommended/cat.json"),
    )

    assert coub_api_auth.friends.get_recommended(q="cat")


def test_get_friend_to_follow__initial(coub_api_auth, requests_mock, snapshot_factory):
    requests_mock.get(
        f"/api/v2/friends/friends_to_follow",
        json=snapshot_factory(f"api/v2/friends/friends_to_follow/initial.json"),
    )

    assert coub_api_auth.friends.to_follow()


def test_get_friend_to_follow__next(coub_api_auth, requests_mock, snapshot_factory):
    requests_mock.get(
        f"/api/v2/friends/friends_to_follow",
        json=snapshot_factory(f"api/v2/friends/friends_to_follow/next.json"),
    )

    assert coub_api_auth.friends.to_follow(req_type="next")
