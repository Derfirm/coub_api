def test_likes_list(coub_api_auth, requests_mock, snapshot_factory, coub_id):
    requests_mock.get(
        f"/api/v2/action_subjects_data/coub_likes_list",
        json=snapshot_factory(f"api/v2/action_subjects_data/coub_likes_list.json"),
    )

    assert coub_api_auth.coub_metadata.likes_list(coub_id)


def test_recoubs_list(coub_api_auth, requests_mock, snapshot_factory, coub_id):
    requests_mock.get(
        f"/api/v2/action_subjects_data/recoubs_list",
        json=snapshot_factory(f"api/v2/action_subjects_data/recoubs_list.json"),
    )
    assert coub_api_auth.coub_metadata.recoubs_list(coub_id)


def test_recoub_list_ids(coub_api_auth, requests_mock, snapshot_factory, coub_id):
    requests_mock.get(
        f"/api/v2/action_subjects_data/recoubs_list",
        json=snapshot_factory(
            f"api/v2/action_subjects_data/recoubs_list_filter_ids.json"
        ),
    )
    assert coub_api_auth.coub_metadata.recoubs_list(coub_id, ids=[4_780_141])


def test_follower_list(coub_api_auth, requests_mock, snapshot_factory):
    channel_id = 313_001
    requests_mock.get(
        f"/api/v2/action_subjects_data/followers_list",
        json=snapshot_factory(f"api/v2/action_subjects_data/followers_list.json"),
    )
    assert coub_api_auth.coub_metadata.followers_list(channel_id)


def test_follower_lis_ids(coub_api_auth, requests_mock, snapshot_factory):
    channel_id = 313_001
    requests_mock.get(
        f"/api/v2/action_subjects_data/followers_list",
        json=snapshot_factory(f"api/v2/action_subjects_data/followers_list_ids.json"),
    )
    assert coub_api_auth.coub_metadata.followers_list(channel_id, ids=[4_051_223])


def test_following_list(coub_api_auth, requests_mock, snapshot_factory):
    channel_id = 313_001
    requests_mock.get(
        f"/api/v2/action_subjects_data/followings_list",
        json=snapshot_factory(f"api/v2/action_subjects_data/followings_list.json"),
    )
    assert coub_api_auth.coub_metadata.followings_list(channel_id)
