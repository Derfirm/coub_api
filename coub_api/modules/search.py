from typing import List

from coub_api.schemas.coub import CoubTags
from coub_api.schemas.search import (
    CoubSearchResponse,
    ChannelSearchResponse,
    GeneralSearchResponse,
)
from .base import BaseConnector

__all__ = ("Search",)


class Search(BaseConnector):
    __slots__ = ()

    def all(
        self,
        q: str,
        *,
        page: int = 1,
        per_page: int = 10,
        order_by: str = "newest_popular",
    ):
        # likes_count, views_count , newest, oldest, newest_popular
        url = self.build_url("/search")
        params = {"q": q, "page": page, "per_page": per_page, "order_by": order_by}
        return GeneralSearchResponse(**self.request("get", url, params=params))

    def channels(
        self, q: str, *, page: int = 1, per_page: int = 10, order_by: str = "newest"
    ):
        # newest, followers_count
        url = self.build_url("/search/channels")
        params = {"q": q, "page": page, "order_by": order_by, "per_page": per_page}
        return ChannelSearchResponse(**self.request("get", url, params=params))

    def coubs(
        self, q: str, *, page: int = 1, per_page: int = 10, order_by: str = "newest"
    ):
        # newest, followers_count
        url = self.build_url("/search/coubs")
        params = {"q": q, "page": page, "order_by": order_by, "per_page": per_page}
        return CoubSearchResponse(**self.request("get", url, params=params))

    def tags(self, title: str) -> List[CoubTags]:
        url = self.build_url("/tags/search")
        params = {"title": title}
        return [CoubTags(**v) for v in self.request("get", url, params=params)]
