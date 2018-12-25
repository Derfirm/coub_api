from coub_api.schemas.coub import BigCoub
from .base import BaseConnector

__all__ = ("Recoub",)


# see https://coub.com/dev/docs/Coub+API%2FRecoubs
class Recoub(BaseConnector):
    __slots__ = ()

    def make(self, recoub_to_id: int, channel_id: int):
        url = self.build_url("/recoubs")
        params = {"recoub_to_id": recoub_to_id, "channel_id": channel_id}
        return BigCoub(**self.authenticated_request("post", url, params=params))

    def delete(self, recoub_id: int, channel_id):
        url = self.build_url("/recoubs")
        params = {"id": recoub_id, "channel_id": channel_id}
        return self.authenticated_request("delete", url, params=params)
