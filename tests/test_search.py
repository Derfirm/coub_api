def test_search_all(coub_api_auth, requests_mock, snapshot_factory, search_q):
    requests_mock.get(
        f"/api/v2/search", json=snapshot_factory(f"api/v2/search/{search_q}.json")
    )
    assert coub_api_auth.search.all(search_q, per_page=5)


def test_search_channel(coub_api_auth, requests_mock, snapshot_factory, search_q):
    requests_mock.get(
        f"/api/v2/search/channels",
        json=snapshot_factory(f"api/v2/search/channels/{search_q}.json"),
    )
    assert coub_api_auth.search.channels(search_q, per_page=5)


def test_search_coubs(coub_api_auth, requests_mock, snapshot_factory, search_q):
    requests_mock.get(
        f"/api/v2/search/coubs",
        json=snapshot_factory(f"api/v2/search/coubs/{search_q}.json"),
    )
    assert coub_api_auth.search.coubs(search_q, per_page=5)
