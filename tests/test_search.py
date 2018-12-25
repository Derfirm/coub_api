def test_search_all(coub_api_auth, requests_mock, snapshot_factory):
    requests_mock.get(
        f"/api/v2/search", json=snapshot_factory(f"api/v2/search/new.json")
    )
    assert coub_api_auth.search.all("new", per_page=5)


def test_search_channel(coub_api_auth, requests_mock, snapshot_factory):
    requests_mock.get(
        f"/api/v2/search/channels",
        json=snapshot_factory(f"api/v2/search/channels/cat.json"),
    )
    assert coub_api_auth.search.channels("cat", per_page=5)


def test_search_coubs(coub_api_auth, requests_mock, snapshot_factory):
    requests_mock.get(
        f"/api/v2/search/coubs", json=snapshot_factory(f"api/v2/search/coubs/cat.json")
    )
    assert coub_api_auth.search.coubs("cat", per_page=5)


def test_search_tags(coub_api_auth, requests_mock, snapshot_factory):
    requests_mock.get(
        f"/api/v2/tags/search", json=snapshot_factory(f"api/v2/search/tags/cat.json")
    )
    assert coub_api_auth.search.tags("cat")
