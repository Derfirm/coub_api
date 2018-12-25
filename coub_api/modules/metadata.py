from typing import List, Optional

from coub_api.schemas.metadata import MetaResponse
from .base import BaseConnector

__all__ = ("MetaData",)


class MetaData(BaseConnector):
    __slots__ = ()

    def likes_list(self, coub_id: int, page: int = 1) -> MetaResponse:
        url = self.build_url("/action_subjects_data/coub_likes_list")
        params = {"id": coub_id, "page": page}
        return MetaResponse(**self.authenticated_request("get", url, params=params))

    def recoubs_list(
        self, coub_id: int, page: int = 1, ids: Optional[List[int]] = None
    ) -> MetaResponse:
        url = self.build_url("/action_subjects_data/recoubs_list")
        params = {"id": coub_id, "page": page}
        if ids:
            assert len(ids) == 1, "coub cant process more than 1 ids"
            params.update({"ids[]": ids[0]})
        return MetaResponse(**self.authenticated_request("get", url, params=params))

    def followers_list(
        self, channel_id: int, page: int = 1, ids: Optional[List[int]] = None
    ) -> MetaResponse:
        url = self.build_url("/action_subjects_data/followers_list")
        params = {"id": channel_id, "page": page}
        if ids:
            assert len(ids) == 1, "coub cant process more than 1 ids"
            params.update({"ids[]": ids[0]})
        return MetaResponse(**self.authenticated_request("get", url, params=params))

    def followings_list(self, channel_id: int, page: int = 1) -> MetaResponse:
        url = self.build_url("/action_subjects_data/followings_list")
        params = {"id": channel_id, "page": page}
        return MetaResponse(**self.authenticated_request("get", url, params=params))
