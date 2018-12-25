from typing import Optional, Dict, Union

from coub_api.schemas.friends import (
    FollowResponse,
    FriendsResponse,
    RecommendedResponse,
)
from coub_api.schemas.constants import Provider
from .base import BaseConnector

__all__ = ("Friends",)


# see https://coub.com/dev/docs/Coub+API%2FFriends
class Friends(BaseConnector):
    __slots__ = ()

    def find(self, provider: Optional[Provider] = None) -> FriendsResponse:
        raise NotImplementedError

    def get_data(
        self, provider: Optional[Provider] = None, *, page: int = 1, per_page: int = 10
    ):
        url = self.build_url("/friends")
        params: Dict[str, Union[str, int]] = {"page": page, "per_page": per_page}
        if provider is not None:
            params.update({"provider": provider})
        return FriendsResponse(**self.authenticated_request("get", url, params=params))

    def get_recommended(
        self, q: str, *, page: int = 1, per_page: int = 10
    ) -> RecommendedResponse:
        url = self.build_url("/friends/recommended")
        params = {"q": q, "page": page, "per_page": per_page}
        return RecommendedResponse(
            **self.authenticated_request("get", url, params=params)
        )

    def to_follow(
        self, *, req_type: str = "initial.json", count: int = 20
    ) -> FollowResponse:
        # req_type may be "initial.json" and "next"
        url = self.build_url("/friends/friends_to_follow")
        params = {"type": req_type, "count": count}
        return FollowResponse(**self.authenticated_request("get", url, params=params))
