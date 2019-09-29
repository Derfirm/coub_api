from coub_api.modules.base import TmpBaseConnector, connector_return_type
from coub_api.schemas.users import UserResponse

__all__ = ("User",)


class User(TmpBaseConnector):
    __slots__ = ()

    def _get_me_response(self) -> connector_return_type:
        url = self.build_url("/users/me")
        return self.authenticated_request("get", url)

    def me(self):
        data = self._get_me_response()
        return UserResponse(**data.json())

    def _get_change_channel_response(self, channel_id: int) -> connector_return_type:
        url = self.build_url("/users/change_channel")
        params = {"channel_id": channel_id}
        return self.authenticated_request("put", url, params=params)

    def change_channel(self, channel_id: int):
        data = self._get_change_channel_response(channel_id)
        return data.json()
