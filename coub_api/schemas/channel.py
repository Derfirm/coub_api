from typing import List, Optional
from datetime import datetime

from pydantic import UrlStr, BaseModel

__all__ = ("ChannelBig", "ChannelSmall", "ChannelResponse", "AvatarVersions")


class AvatarVersions(BaseModel):
    template: UrlStr
    versions: Optional[List[str]]


class ChannelSmall(BaseModel):
    id: int
    permalink: str
    title: str
    description: Optional[str]
    followers_count: int
    following_count: int
    avatar_versions: AvatarVersions
    # only if auth
    i_follow_him: Optional[bool]


# see https://coub.com/dev/docs/data+structures/channel+big+json
# response describe non-auth request
# (excluded i_follow_him, he_follows_me and some other fields)
class ChannelBig(BaseModel):
    from .coub import BigCoub

    class Authentication(BaseModel):
        id: int
        channel_id: int
        provider: str
        username_from_provider: str

    class Meta(BaseModel):
        description: Optional[str]
        homepage: Optional[str]
        twitter: Optional[str]
        facebook: Optional[str]
        tumblr: Optional[str]
        youtube: Optional[str]
        vimeo: Optional[str]

    class Contacts(BaseModel):
        homepage: Optional[str]
        tumblr: Optional[str]
        youtube: Optional[str]
        vimeo: Optional[str]

    simple_coubs_count: Optional[int]
    id: int
    user_id: int
    permalink: str
    title: str
    description: Optional[str]
    contacts: Optional[Contacts]
    created_at: datetime
    updated_at: datetime
    avatar_versions: AvatarVersions
    followers_count: int
    following_count: int
    recoubs_count: int
    likes_count: int
    stories_count: Optional[int]
    authentications: Optional[List[Authentication]]
    background_coub: Optional[BigCoub]
    background_image: Optional[str]
    timeline_banner_image: Optional[str]
    meta: Meta
    views_count: int
    hide_owner: bool


class ChannelResponse(BaseModel):
    redirect_url: UrlStr
    channel: ChannelBig
