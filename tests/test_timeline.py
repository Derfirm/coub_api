from itertools import product

import pytest

from coub_api.schemas.constants import Period, Section, Category, FeaturedSection


@pytest.mark.parametrize("period", Period)
def test_hot__period(coub_api, requests_mock, snapshot_factory, period):
    requests_mock.get(
        f"/api/v2/timeline/subscriptions/{period}",
        json=snapshot_factory(f"api/v2/timeline/subscriptions/{period}.json"),
    )

    assert coub_api.timeline.hot(period=period)


@pytest.mark.parametrize("section", Section)
def test_hot__section(coub_api, requests_mock, snapshot_factory, section):
    requests_mock.get(
        f"/api/v2/timeline/subscriptions/{section}",
        json=snapshot_factory(f"api/v2/timeline/subscriptions/{section}.json"),
    )

    assert coub_api.timeline.hot(section=section)


def test_hot__section_and_period(coub_api):
    with pytest.raises(ValueError):
        coub_api.timeline.hot(section=Section.NEWEST, period=Period.QUARTER)


@pytest.mark.parametrize(
    "category, period",
    product(
        set(Category.__members__.values()) - {Category.ALL}, Period.__members__.values()
    ),
)
def test_community(coub_api, requests_mock, snapshot_factory, category, period):
    requests_mock.get(
        f"/api/v2/timeline/community/{category}/{period}",
        json=snapshot_factory(f"api/v2/timeline/community/{category}/{period}.json"),
    )

    assert coub_api.timeline.community(category, period=period)


@pytest.mark.parametrize(
    "section, category",
    product(
        Section.__members__.values(),
        set(Category.__members__.values()) - {Category.ALL},
    ),
)
def test_community__section(
    coub_api, requests_mock, snapshot_factory, section, category
):
    requests_mock.get(
        f"/api/v2/timeline/community/{category}/{section}",
        json=snapshot_factory(f"api/v2/timeline/community/{category}/{section}.json"),
    )

    assert coub_api.timeline.community(category, section=section)


def test_section_and_period(coub_api,):
    with pytest.raises(ValueError):
        coub_api.timeline.community(
            Category.NEWS, section=Section.NEWEST, period=Period.QUARTER
        )


def test_section__category_all(coub_api,):
    with pytest.raises(ValueError):
        coub_api.timeline.community(Category.ALL, section=Section.NEWEST)


def test_channel(coub_api, requests_mock, snapshot_factory, channel_id):
    requests_mock.get(
        f"/api/v2/timeline/channel/{channel_id}",
        json=snapshot_factory(f"api/v2/timeline/channel/{channel_id}.json"),
    )
    assert coub_api.timeline.channel(channel_id, per_page=5)


def test_feed(coub_api, requests_mock, snapshot_factory, tag_name):
    requests_mock.get(
        f"/api/v2/timeline/tag/{tag_name}",
        json=snapshot_factory(f"api/v2/timeline/tag/{tag_name}.json"),
    )
    assert coub_api.timeline.tag_feed(tag_name, per_page=5)


def test_user(coub_api_auth, requests_mock, snapshot_factory):
    requests_mock.get("/api/v2/timeline", json=snapshot_factory("api/v2/timeline.json"))
    assert coub_api_auth.timeline.user(per_page=1)


def test_me_liked(coub_api_auth, requests_mock, snapshot_factory):
    requests_mock.get(
        "/api/v2/timeline/likes", json=snapshot_factory("api/v2/timeline/likes.json")
    )
    assert coub_api_auth.timeline.me_liked(per_page=5)


@pytest.mark.parametrize("feature_section", [FeaturedSection.NEWEST])
def test_feature__section(coub_api, requests_mock, snapshot_factory, feature_section):
    requests_mock.get(
        "/api/v2/timeline/explore",
        json=snapshot_factory("api/v2/timeline/explore.json"),
    )

    assert coub_api.timeline.featured(feature_section)


@pytest.mark.parametrize(
    "feature_section", [FeaturedSection.TOP_OF_THE_MONTH, FeaturedSection.UNDERVALUED]
)
def test_feature__section(coub_api, requests_mock, snapshot_factory, feature_section):
    requests_mock.get(
        "/api/v2/timeline/explore",
        json=snapshot_factory(f"api/v2/timeline/explore/{feature_section}.json"),
    )

    assert coub_api.timeline.featured(feature_section)


def test_editor_choice(coub_api, requests_mock, snapshot_factory):
    requests_mock.get(
        "/api/v2/timeline/channel/royal.coubs",
        json=snapshot_factory(f"api/v2/timeline/channel/royal.coubs.json"),
    )
    assert coub_api.timeline.editor_choice(order_by="oldest", per_page=5)


def test_coub_of_the_day(coub_api, requests_mock, snapshot_factory):
    requests_mock.get(
        "/api/v2/timeline/channel/oftheday",
        json=snapshot_factory(f"api/v2/timeline/channel/oftheday.json"),
    )
    assert coub_api.timeline.coub_of_the_day(order_by="newset", per_page=9)
