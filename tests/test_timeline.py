from coub_api.schemas.constants import Period, Section, Category


def test_hot__default(coub_api, requests_mock, snapshot_factory):
    requests_mock.get(
        "/api/v2/timeline/hot/", json=snapshot_factory(f"api/v2/timeline/hot.json")
    )

    assert coub_api.timeline.hot()


def test_hot__category(coub_api, requests_mock, snapshot_factory):
    category = Category.DANCE
    requests_mock.get(
        f"/api/v2/timeline/hot/{category}",
        json=snapshot_factory(f"api/v2/timeline/hot/{category}.json"),
    )

    assert coub_api.timeline.hot(category=category)


def test_hot__period(coub_api, requests_mock, snapshot_factory):
    period = Period.WEEKLY
    requests_mock.get(
        f"/api/v2/timeline/hot/{period}",
        json=snapshot_factory(f"api/v2/timeline/hot/{period}.json"),
    )

    assert coub_api.timeline.hot(period=period)


def test_hot__period_category(coub_api, requests_mock, snapshot_factory):
    period = Period.MONTHLY
    category = Category.CARS
    requests_mock.get(
        f"/api/v2/timeline/hot/{category}/{period}",
        json=snapshot_factory(f"api/v2/timeline/hot/{category}+{period}.json"),
    )

    assert coub_api.timeline.hot(category=category, period=period)


def test_section__default(coub_api, requests_mock, snapshot_factory):
    section = Section.RISING
    requests_mock.get(
        f"/api/v2/timeline/explore/{section}/",
        json=snapshot_factory(f"api/v2/timeline/section/{section}.json"),
    )

    assert coub_api.timeline.section(section)


def test_section__category(coub_api, requests_mock, snapshot_factory):
    section = Section.RISING
    category = Category.CARS
    requests_mock.get(
        f"/api/v2/timeline/{section}/{category}",
        json=snapshot_factory(f"api/v2/timeline/section/{section}+{category}.json"),
    )

    assert coub_api.timeline.section(section, category=category)


def test_user(coub_api_auth, requests_mock, snapshot_factory):
    requests_mock.get(
        "/api/v2/timeline", json=snapshot_factory("api/v2/timeline/user.json")
    )
    assert coub_api_auth.timeline.user(per_page=1)


def test_channel(coub_api, requests_mock, snapshot_factory):
    channel_id = 300_001
    requests_mock.get(
        f"/api/v2/timeline/channel/{channel_id}",
        json=snapshot_factory(f"api/v2/timeline/channel/{channel_id}.json"),
    )
    assert coub_api.timeline.channel(channel_id, per_page=5)


def test_feed(coub_api, requests_mock, snapshot_factory):
    tag_name = "catgirl"
    requests_mock.get(
        f"/api/v2/timeline/tag/{tag_name}",
        json=snapshot_factory(f"api/v2/timeline/tag/{tag_name}.json"),
    )
    assert coub_api.timeline.tag_feed(tag_name, per_page=5)


def test_me_liked(coub_api_auth, requests_mock):

    requests_mock.get(
        "/api/v2/timeline/likes",
        json={"page": 1, "per_page": 5, "total_pages": 0, "coubs": []},
    )
    assert coub_api_auth.timeline.me_liked(per_page=5)
