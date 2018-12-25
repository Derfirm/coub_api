from typing import List

from pydantic import BaseModel

from .channel import ChannelSmall

__all__ = ("MetaResponse",)


class MetaResponse(BaseModel):
    page: int
    total_pages: int
    channels: List[ChannelSmall]
