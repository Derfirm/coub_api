import json
from pathlib import Path
from functools import lru_cache

import pytest

from coub_api import CoubApi
from tests import _BASE_PATH  # noqa
from tools.utils import extract_params_from_file


@pytest.fixture
def coub_api() -> CoubApi:
    return CoubApi()


@pytest.fixture
def coub_id():
    return 95_639_280


@pytest.fixture
def token() -> str:
    return "811519e2e0aacdc520c46a01c95f0dc61a4cfb48a077e7c29284cdc9aa02de85"


@pytest.fixture
def coub_api_auth(coub_api: CoubApi, token: str) -> CoubApi:
    api = coub_api
    api.authenticate(token)
    return api


@pytest.fixture
def snapshot_factory():
    base_path = _BASE_PATH / "snapshots"

    @lru_cache(maxsize=None)
    def get_snapshot(path: str):
        with (base_path / Path(path)).open() as f:
            return json.load(f)

    return get_snapshot


@pytest.fixture(
    params=extract_params_from_file(_BASE_PATH / "snapshots/config.json", "coubs_list")
)
def coub_permalink(request):
    return request.param


@pytest.fixture(
    params=extract_params_from_file(
        _BASE_PATH / "snapshots/config.json", "channels_list"
    )
)
def channel_id(request):
    return request.param


@pytest.fixture(
    params=extract_params_from_file(_BASE_PATH / "snapshots/config.json", "tag_list")
)
def tag_name(request):
    return request.param


@pytest.fixture(
    params=extract_params_from_file(_BASE_PATH / "snapshots/config.json", "search_list")
)
def search_q(request):
    return request.param
