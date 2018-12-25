from coub_api.schemas.timeline import TimeLineResponse, SectionTimeLineResponse
from coub_api.schemas.constants import Period, Section, Category
from .base import BaseConnector

__all__ = ("Timeline",)


class Timeline(BaseConnector):
    __slots__ = ()

    def hot(
        self,
        *,
        order_by: str = "newest_popular",
        category: Category = Category.ALL,
        period: Period = Period.DAILY,
        page: int = 1,
        per_page: int = 10,
    ) -> SectionTimeLineResponse:
        # order_by: likes_count, views_count, newest_popular, oldest
        if category and period:
            _path = f"{category}/{period}"
        else:
            _path = category or period

        url = self.build_url(f"/timeline/hot/{_path}")
        params = {"order_by": order_by, "per_page": per_page, "page": page}
        return SectionTimeLineResponse(**self.request("get", url, params=params))

    def section(
        self,
        section: Section,
        *,
        category: Category = Category.ALL,
        page: int = 1,
        per_page: int = 10,
    ) -> SectionTimeLineResponse:
        if category == Category.ALL:
            _path = f"explore/{section}/"
        else:
            _path = f"{section}/{category}"

        url = self.build_url(f"/timeline/{_path}")
        params = {"per_page": per_page, "page": page}
        return SectionTimeLineResponse(**self.request("get", url, params=params))

    def user(self, *, page: int = 1, per_page: int = 10) -> TimeLineResponse:
        url = self.build_url("/timeline")
        params = {"page": page, "per_page": per_page}
        return TimeLineResponse(**self.authenticated_request("get", url, params=params))

    def channel(
        self,
        channel_id: int,
        *,
        page: int = 1,
        per_page: int = 10,
        order_by: str = "views_count",
    ) -> TimeLineResponse:
        # likes_count, views_count, newest_popular.
        url = self.build_url(f"/timeline/channel/{channel_id}")
        params = {"page": page, "per_page": per_page, "order_by": order_by}
        return TimeLineResponse(**self.request("get", url, params=params))

    def tag_feed(
        self,
        tag_name: str,
        *,
        page: int = 1,
        per_page: int = 10,
        order_by: str = "oldest",
    ) -> TimeLineResponse:
        # likes_count, views_count, newest_popular, oldest
        url = self.build_url(f"/timeline/tag/{tag_name}")
        params = {"page": page, "per_page": per_page, "order_by": order_by}
        return TimeLineResponse(**self.request("get", url, params=params))

    def me_liked(self, *, page: int = 1, per_page: int = 10) -> TimeLineResponse:
        url = self.build_url("/timeline/likes")
        params = {"page": page, "per_page": per_page}
        return TimeLineResponse(**self.authenticated_request("get", url, params=params))
