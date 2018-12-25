from typing import Optional

from .modules.user import User
from .modules.coubs import Coubs
from .modules.likes import Likes
from .modules.recoub import Recoub
from .modules.search import Search
from .modules.channel import Channel
from .modules.follows import Follow
from .modules.friends import Friends
from .modules.metadata import MetaData
from .modules.timelines import Timeline
from .modules.notifications import Notifications

__all__ = ("CoubApi",)


class CoubApi:
    __slots__ = ("token",)

    def __init__(self):
        self.token: Optional[str] = None

    def authenticate(self, token: str):
        self.token = token

    @property
    def timeline(self):
        return Timeline(self.token)

    @property
    def coubs(self):
        return Coubs(self.token)

    @property
    def recoubs(self):
        return Recoub(self.token)

    @property
    def channels(self):
        return Channel(self.token)

    @property
    def likes(self):
        return Likes(self.token)

    @property
    def following(self):
        return Follow(self.token)

    @property
    def coub_metadata(self):
        return MetaData(self.token)

    @property
    def users(self):
        return User(self.token)

    @property
    def friends(self):
        return Friends(self.token)

    @property
    def notification(self):
        return Notifications(self.token)

    @property
    def search(self):
        return Search(self.token)
