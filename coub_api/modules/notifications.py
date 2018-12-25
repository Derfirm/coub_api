from .base import BaseConnector

__all__ = ("Notifications",)


class Notifications(BaseConnector):
    __slots__ = ()

    def get_list(self, *, page: int = 1, per_page: int = 10):
        url = self.build_url("/notifications")
        params = {"page": page, "per_page": per_page}
        return self.authenticated_request("get", url, params=params)

    def set_viewed(self):
        raise NotImplementedError
        url = self.build_url("/channels/notifications_viewed")
        headers = {"access_token": self.token}
        return self.authenticated_request("get", url, headers=headers)
