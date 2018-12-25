from typing import Optional

from coub_api.schemas.channel import ChannelBig, ChannelResponse
from .base import BaseConnector

__all__ = ("Channel",)


# https://coub.com/dev/docs/Coub+API%2FChannels
class Channel(BaseConnector):
    __slots__ = ()

    def get_data(self, channel_id: int):
        url = self.build_url(f"/channels/{channel_id}")
        return self.request("get", url)

    def create(self, title: str, permalink: str, category: str):
        if len(permalink) < 8:
            raise ValueError(f"To short permalink {permalink}, required min 8 symbols")

        url = self.build_url("/channels")
        params = {
            "channels[title]": title,
            "channels[permalink]": permalink,
            "channels[category]": category,
        }
        return ChannelResponse(**self.authenticated_request("post", url, params=params))

    def delete(self, channel_id: int):
        url = self.build_url(f"/channels/{channel_id}")
        return ChannelResponse(**self.authenticated_request("delete", url))

    def update_data(self):
        raise NotImplementedError
        url = self.build_url("/channels/update_info")
        params = {}
        return self.authenticated_request("put", url, params=params)

    # TODO
    def change_avatar(self, channel_id: int, image_path: str):
        # raise NotImplementedError
        # import base64

        # with open(image_path, "rb") as image_file:
        #     encoded_string = base64.b64encode(image_file.read())

        url = self.build_url("/channels/upload_avatar")
        params = {
            # "utf8": True,
            "channels[id]": channel_id,
            # "channels[avatar]": encoded_string
            # "channels[avatar]":  encoded_string
            # "authenticity_token": self.token
        }
        data = {"channels[avatar]": open(image_path, "rb")}
        self.authenticated_request("post", url, params=params, data=data)
        # return ChannelBig(**self.authenticated_request("post", url, files=files))

    def delete_avatar(self, channel_id: int):
        url = self.build_url("/channels/delete_avatar")
        params = {"channels[id]": channel_id}
        return ChannelBig(**self.authenticated_request("delete", url, params=params))

    # TODO
    def add_background(
        self, channel_id: int, coub_permalink: Optional[str], image_path: Optional[str]
    ):
        if coub_permalink and image_path:
            raise ValueError("only one params is required!")

        if coub_permalink:
            params = {"background[coub]": coub_permalink}
        else:
            params = {}

        url = self.build_url(f"channels/{channel_id}/backgrounds")
        return self.authenticated_request("post", url, params=params)

    def change_background_position(self, channel_id: int, offset_y: float):
        url = self.build_url(f"channels/{channel_id}/backgrounds")
        params = {"offset_y": offset_y}
        return self.authenticated_request("post", url, params=params)["status"]

    def delete_background(self, channel_id: int):
        url = self.build_url(f"channels/{channel_id}/backgrounds")
        return self.authenticated_request("delete", url)["status"]

    # TODO channels Recommendation
