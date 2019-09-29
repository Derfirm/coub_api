import os
import json
import uuid
from typing import Set, Optional
from urllib.parse import urlparse

from coub_api import CoubApi
from coub_api.schemas.constants import Period, Section, Category, FeaturedSection
from tests import _BASE_PATH  # noqa
from tools.utils import extract_params_from_file


def anonymize_data(data, keys: Set[str]):
    for key in keys & data.keys():
        data[key] = uuid.uuid4().hex
    return data


def normalize_path_from_url(url: str) -> str:
    path = urlparse(url).path

    if not path:
        raise ValueError("path cannot be empty")
    if path.startswith("/"):
        path = path[1:]
    if path.endswith("/"):
        path = path[:-1]
    return path


def save_snapshot(path: str, filename: str, data):
    p = _BASE_PATH / "snapshots" / path
    p.mkdir(parents=True, exist_ok=True)
    q = p / f"{filename}.json"
    data = anonymize_data(data, keys={"api_token"})
    q.open("w").write(json.dumps(data))


def base_snapshot_processing(response, filename: Optional[str] = None):
    path = normalize_path_from_url(response.url)
    if not filename:
        path, filename = path.rsplit("/", 1)
    data = response.json()
    save_snapshot(path, filename, data)


def download_coub(api: CoubApi, *, coub_id: str):
    response = api.coubs._get_coub_response(coub_id)
    base_snapshot_processing(response)


def download_hot_timeline(api: CoubApi, *, period: Period, page: int, per_page: int):
    response = api.timeline._get_hot_response(
        order_by="newest_popular", postfix=period, page=page, per_page=per_page
    )
    base_snapshot_processing(response)


def download_hot_timeline_section(
    api: CoubApi, *, section: Section, page: int, per_page: int
):
    response = api.timeline._get_hot_response(
        order_by="newest_popular", postfix=section, page=page, per_page=per_page
    )

    base_snapshot_processing(response)


def download_community_period(
    api: CoubApi, *, category: Category, period: Period, page: int, per_page: int
):
    response = api.timeline._get_community_response(
        category=category, postfix=period, page=page, per_page=per_page
    )
    base_snapshot_processing(response)


def download_community_section(
    api: CoubApi, *, category: Category, section: Section, page: int, per_page: int
):
    response = api.timeline._get_community_response(
        postfix=section, category=category, page=page, per_page=per_page
    )
    base_snapshot_processing(response)


def download_user_timeline(api: CoubApi, page: int, per_page: int):
    response = api.timeline._get_user_response(page=page, per_page=per_page)
    base_snapshot_processing(response)


def download_channel_timeline(api: CoubApi, channel_id, page, per_page):
    response = api.timeline._get_channel_response(
        channel_id, page=page, per_page=per_page, order_by="views_count"
    )
    base_snapshot_processing(response)


def download_timeline_tag(api: CoubApi, *, tag_name: str, page: int, per_page: int):
    response = api.timeline._get_tag_response(
        tag_name, page=page, per_page=per_page, order_by="likes_count"
    )
    base_snapshot_processing(response)


def download_me_liked(api: CoubApi, per_page: int, page: int):
    response = api.timeline._get_me_liked_response(page=page, per_page=per_page)
    base_snapshot_processing(response)


def download_featured_timeline(
    api: CoubApi, *, feature_section: FeaturedSection, page: int, per_page: int
):
    response = api.timeline._get_featured_response(
        feature_section, page=page, per_page=per_page
    )
    base_snapshot_processing(response, filename=feature_section)


def download_search_all(api: CoubApi, q: str, page: int, per_page: int):
    response = api.search._get_all_response(
        q=q, page=page, per_page=per_page, order_by="newest_popular"
    )
    base_snapshot_processing(response, filename=q)


def download_search_coub(api: CoubApi, q: str, page: int, per_page: int):
    response = api.search._get_coubs_response(
        q=q, page=page, per_page=per_page, order_by="newest_popular"
    )
    base_snapshot_processing(response, filename=q)


def download_search_channel(api: CoubApi, q: str, page: int, per_page: int):
    response = api.search._get_channels_response(
        q=q, page=page, per_page=per_page, order_by="newest_popular"
    )
    base_snapshot_processing(response, filename=q)


def download_users_me(api: CoubApi,):
    response = api.users._get_me_response()
    base_snapshot_processing(response)


def download_user_chahge_channel(api: CoubApi, channel_id: int):
    response = api.users._get_change_channel_response(channel_id)
    base_snapshot_processing(response)


if __name__ == "__main__":
    access_token = os.environ.get("coub_access_token")
    api = CoubApi()
    api.authenticate(access_token)

    for coub_id in extract_params_from_file(
        _BASE_PATH / "snapshots/config.json", "coubs_list"
    ):
        download_coub(api, coub_id=coub_id)

    for period in Period.__members__.values():
        download_hot_timeline(api, period=period, page=1, per_page=50)

    for section in Section.__members__.values():
        download_hot_timeline_section(api, section=section, page=1, per_page=50)

    for category in Category.__members__.values():
        if category == Category.ALL:
            continue

        for period in Period.__members__.values():
            download_community_period(
                api, category=category, period=period, page=1, per_page=50
            )
        for section in Section.__members__.values():
            download_community_section(
                api, category=category, section=section, page=1, per_page=50
            )

    download_user_timeline(api, page=1, per_page=50)

    for channel_id in extract_params_from_file(
        _BASE_PATH / "snapshots/config.json", "channels_list"
    ):
        download_channel_timeline(api, channel_id=channel_id, page=1, per_page=50)

    for tag_name in extract_params_from_file(
        _BASE_PATH / "snapshots/config.json", "tag_list"
    ):
        download_timeline_tag(api, tag_name=tag_name, page=1, per_page=50)

    download_me_liked(api, page=1, per_page=10)

    for feature in FeaturedSection.__members__.values():
        download_featured_timeline(api, feature_section=feature, page=1, per_page=50)

    for q in extract_params_from_file(
        _BASE_PATH / "snapshots/config.json", "search_list"
    ):
        download_search_all(api, q=q, page=1, per_page=20)
        download_search_coub(api, q=q, page=1, per_page=20)
        download_search_channel(api, q=q, page=1, per_page=20)
    download_users_me(api)
    download_user_chahge_channel(api, channel_id=313669)
