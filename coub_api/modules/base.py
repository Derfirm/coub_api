from typing import Optional
from urllib.parse import urljoin

import requests

from coub_api._urls import API_PATH, COUB_URL

__all__ = ("BaseConnector",)


class BaseConnector:
    __slots__ = ("token",)

    def __init__(self, token: Optional[str] = None):
        self.token = token

    @staticmethod
    def build_url(path: str) -> str:
        return urljoin(COUB_URL, f"{API_PATH}{path}")

    @staticmethod
    def request(method: str, url: str, **kwargs):
        response = requests.request(method, url, **kwargs)
        response.raise_for_status()
        data = response.json()
        return data

    def authenticated_request(
        self, method: str, url: str, *, params: Optional[dict] = None, **kwargs
    ):
        if self.token is None:
            raise ValueError("token required")

        params = params or {}
        params.update({"access_token": self.token})
        return self.request(method, url, params=params, **kwargs)
