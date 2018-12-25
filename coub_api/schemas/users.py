import enum
from typing import List, Optional
from datetime import datetime

from pydantic import BaseModel

from .channel import ChannelBig, ChannelSmall


@enum.unique
class Sex(str, enum.Enum):
    MALE = "male"
    FEMALE = "female"
    UNSPECIFIED = "unspecified"


class UserResponse(BaseModel):
    id: int
    permalink: str
    name: str
    sex: Sex
    city: Optional[str]
    current_channel: ChannelSmall
    created_at: datetime
    updated_at: datetime
    api_token: str
    # unsubscribed_fields
    has_linked_vine_accounts: bool
    likes_count: int
    favourites_count: int
    channels: List[ChannelBig]
