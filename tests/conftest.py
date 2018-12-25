import json
from pathlib import Path
from functools import lru_cache

import pytest

from coub_api import CoubApi


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
    base_path = Path("tests/snapshots")

    @lru_cache(maxsize=None)
    def get_snapshot(path: str):
        with (base_path / Path(path)).open() as f:
            return json.load(f)

    return get_snapshot
