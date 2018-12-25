from .base import BaseConnector

__all__ = ("Likes",)


# see https://coub.com/dev/docs/Coub+API%2FLikes
class Likes(BaseConnector):
    __slots__ = ()

    def do_like(self, coub_id: int, from_channel_id: int):
        url = self.build_url("/likes")
        params = {"id": coub_id, "channel_id": from_channel_id}
        return self.authenticated_request("post", url, params=params)

    def unlike(self, coub_id: int, from_channel_id: int):
        url = self.build_url("/likes")
        params = {"id": coub_id, "channel_id": from_channel_id}
        return self.authenticated_request("delete", url, params=params)
