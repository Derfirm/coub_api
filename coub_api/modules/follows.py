from .base import BaseConnector

__all__ = ("Follow",)


# see https://coub.com/dev/docs/Coub+API%2FFollowing
class Follow(BaseConnector):
    __slots__ = ()

    def follow(self, user_id: int, channel_id: int):
        url = self.build_url("/follows")
        params = {"id": user_id, "channel_id": channel_id}
        return self.authenticated_request("post", url, params=params)

    def unfollow(self, user_id: int, channel_id: int):
        url = self.build_url("/follows")
        params = {"id": user_id, "channel_id": channel_id}
        return self.authenticated_request("delete", url, params=params)
