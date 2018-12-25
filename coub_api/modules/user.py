from coub_api.schemas.users import UserResponse
from .base import BaseConnector

__all__ = ("User",)


class User(BaseConnector):
    __slots__ = ()

    def me(self):
        url = self.build_url("/users/me")
        return UserResponse(**self.authenticated_request("get", url))

    def change_channel(self, channel_id: int):
        url = self.build_url("/users/change_channel")
        params = {"channel_id": channel_id}
        return self.authenticated_request("put", url, params=params)
