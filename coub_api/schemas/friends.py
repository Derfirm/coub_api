from typing import List

from pydantic import BaseModel

from .channel import ChannelSmall

__all__ = ("FriendsResponse", "FollowResponse", "RecommendedResponse")


class FriendsResponse(BaseModel):
    page: int
    total_pages: int
    total_friends: int
    per_page: int
    friends: List[ChannelSmall]


class FollowResponse(BaseModel):
    friends: List[ChannelSmall]


class RecommendedResponse(BaseModel):
    channels: List[ChannelSmall]
