from typing import Optional
from urllib.parse import urljoin

import requests

from coub_api._urls import API_PATH, COUB_URL

__all__ = ("BaseConnector", "TmpBaseConnector", "connector_return_type")

connector_return_type = requests.Response


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


class TmpBaseConnector:
    __slots__ = ("token",)

    def __init__(self, token: Optional[str] = None) -> None:
        self.token = token

    @staticmethod
    def build_url(path: str) -> str:
        return urljoin(COUB_URL, f"{API_PATH}{path}")

    @staticmethod
    def request(method: str, url: str, **kwargs) -> connector_return_type:
        response = requests.request(method, url, **kwargs)
        response.raise_for_status()
        return response

    def authenticated_request(
        self, method: str, url: str, *, params: Optional[dict] = None, **kwargs
    ) -> connector_return_type:
        if self.token is None:
            raise ValueError("token required")

        params = params or {}
        params.update({"access_token": self.token})
        return self.request(method, url, params=params, **kwargs)
