from typing import Union, Optional

from coub_api.modules.base import TmpBaseConnector, connector_return_type
from coub_api.schemas.timeline import (
    TimeLineResponse,
    MyTimeLineResponse,
    SectionTimeLineResponse,
)
from coub_api.schemas.constants import Period, Section, Category, FeaturedSection

__all__ = ("Timeline",)


class Timeline(TmpBaseConnector):
    __slots__ = ()

    def _get_hot_response(
        self,
        *,
        order_by: str,
        postfix: Union[Period, Section],
        page: int,
        per_page: int,
    ) -> connector_return_type:
        # order_by: likes_count, views_count, newest_popular, oldest
        url = self.build_url(f"/timeline/subscriptions/{postfix}")
        params = {"order_by": order_by, "per_page": per_page, "page": page}
        return self.request("get", url, params=params)

    def hot(
        self,
        *,
        order_by: str = "newest_popular",
        period: Period = Period.DAILY,
        section: Optional[Section] = None,
        page: int = 1,
        per_page: int = 10,
    ) -> SectionTimeLineResponse:
        if section and period != Period.DAILY:
            raise ValueError("cant setup section and period in one time")
        postfix = section or period
        data = self._get_hot_response(
            order_by=order_by, postfix=postfix, page=page, per_page=per_page
        )
        return SectionTimeLineResponse(**data.json())

    def _get_community_response(
        self,
        *,
        postfix: Union[Period, Section],
        category: Category,
        page: int,
        per_page: int,
    ) -> connector_return_type:
        if category == Category.ALL:
            raise ValueError("please, select concrete category")

        _path = f"{category}/{postfix}"
        url = self.build_url(f"/timeline/community/{_path}")
        params = {"per_page": per_page, "page": page}
        return self.request("get", url, params=params)

    def community(
        self,
        category: Category,
        *,
        section: Optional[Section] = None,
        period: Period = Period.DAILY,
        page: int = 1,
        per_page: int = 10,
    ) -> SectionTimeLineResponse:
        if section and period != Period.DAILY:
            raise ValueError("cant setup section and period in one time")
        postfix = section or period
        data = self._get_community_response(
            category=category, postfix=postfix, page=page, per_page=per_page
        )
        return SectionTimeLineResponse(**data.json())

    def _get_user_response(self, *, page: int, per_page: int) -> connector_return_type:
        url = self.build_url("/timeline")
        params = {"page": page, "per_page": per_page}
        return self.authenticated_request("get", url, params=params)

    def user(self, *, page: int = 1, per_page: int = 10) -> MyTimeLineResponse:
        data = self._get_user_response(page=page, per_page=per_page)
        return MyTimeLineResponse(**data.json())

    def _get_channel_response(
        self, channel_id: Union[int, str], *, page: int, per_page: int, order_by: str
    ) -> connector_return_type:
        # likes_count, views_count, newest, oldest, random.
        url = self.build_url(f"/timeline/channel/{channel_id}")
        params = {"page": page, "per_page": per_page, "order_by": order_by}
        return self.request("get", url, params=params)

    def channel(
        self,
        channel_id: Union[int, str],
        *,
        page: int = 1,
        per_page: int = 10,
        order_by: str = "views_count",
    ) -> TimeLineResponse:
        data = self._get_channel_response(
            channel_id=channel_id, page=page, per_page=per_page, order_by=order_by
        )
        return TimeLineResponse(**data.json())

    def _get_featured_response(
        self, feature_section: FeaturedSection, page: int, per_page: int
    ) -> connector_return_type:
        url = self.build_url("/timeline/explore")
        params = {"order_by": feature_section, "per_page": per_page, "page": page}
        return self.request("get", url, params=params)

    def featured(
        self,
        feature_section: FeaturedSection = FeaturedSection.NEWEST,
        *,
        page: int = 1,
        per_page: int = 10,
    ):
        data = self._get_featured_response(
            feature_section, page=page, per_page=per_page
        )
        return TimeLineResponse(**data.json())

    def _get_tag_response(
        self, tag_name: str, *, page: int, per_page: int, order_by: str
    ) -> connector_return_type:
        # likes_count, views_count, newest, oldest
        url = self.build_url(f"/timeline/tag/{tag_name}")
        params = {"page": page, "per_page": per_page, "order_by": order_by}
        return self.request("get", url, params=params)

    def tag_feed(
        self,
        tag_name: str,
        *,
        page: int = 1,
        per_page: int = 10,
        order_by: str = "oldest",
    ) -> TimeLineResponse:
        data = self._get_tag_response(
            tag_name, page=page, per_page=per_page, order_by=order_by
        )
        return TimeLineResponse(**data.json())

    def _get_me_liked_response(
        self, *, page: int, per_page: int
    ) -> connector_return_type:
        url = self.build_url("/timeline/likes")
        params = {"page": page, "per_page": per_page}
        return self.authenticated_request("get", url, params=params)

    def me_liked(self, *, page: int = 1, per_page: int = 10) -> MyTimeLineResponse:
        data = self._get_me_liked_response(page=page, per_page=per_page)
        return MyTimeLineResponse(**data.json())

    def editor_choice(
        self, *, order_by: str = "views_count", page: int = 1, per_page: int = 10
    ) -> TimeLineResponse:
        return self.channel(
            "royal.coubs", per_page=per_page, order_by=order_by, page=page
        )

    def coub_of_the_day(
        self, *, order_by: str = "views_count", page: int = 1, per_page: int = 10
    ) -> TimeLineResponse:
        return self.channel("oftheday", per_page=per_page, order_by=order_by, page=page)
