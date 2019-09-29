from coub_api.modules.base import TmpBaseConnector, connector_return_type
from coub_api.schemas.search import (
    CoubSearchResponse,
    ChannelSearchResponse,
    GeneralSearchResponse,
)

__all__ = ("Search",)


class Search(TmpBaseConnector):
    __slots__ = ()

    def _get_all_response(
        self, q: str, *, page: int, per_page: int, order_by: str
    ) -> connector_return_type:
        # likes_count, views_count , newest, oldest, newest_popular
        url = self.build_url("/search")
        params = {"q": q, "page": page, "per_page": per_page, "order_by": order_by}
        return self.request("get", url, params=params)

    def all(
        self,
        q: str,
        *,
        page: int = 1,
        per_page: int = 10,
        order_by: str = "newest_popular",
    ):
        data = self._get_all_response(
            q, page=page, per_page=per_page, order_by=order_by
        )
        return GeneralSearchResponse(**data.json())

    def _get_channels_response(
        self, q: str, *, page: int, per_page: int, order_by: str
    ) -> connector_return_type:
        # newest, followers_count
        url = self.build_url("/search/channels")
        params = {"q": q, "page": page, "order_by": order_by, "per_page": per_page}
        return self.request("get", url, params=params)

    def channels(
        self, q: str, *, page: int = 1, per_page: int = 10, order_by: str = "newest"
    ):
        data = self._get_channels_response(
            q, page=page, per_page=per_page, order_by=order_by
        )
        return ChannelSearchResponse(**data.json())

    def _get_coubs_response(
        self, q: str, *, page: int, per_page: int, order_by: str
    ) -> connector_return_type:
        # newest, followers_count
        url = self.build_url("/search/coubs")
        params = {"q": q, "page": page, "order_by": order_by, "per_page": per_page}
        return self.request("get", url, params=params)

    def coubs(
        self, q: str, *, page: int = 1, per_page: int = 10, order_by: str = "newest"
    ):
        data = self._get_coubs_response(
            q, page=page, per_page=per_page, order_by=order_by
        )
        return CoubSearchResponse(**data.json())
