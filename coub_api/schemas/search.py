from typing import List

from pydantic import BaseModel

__all__ = ("GeneralSearchResponse", "CoubSearchResponse", "ChannelSearchResponse")


class GeneralSearchResponse(BaseModel):
    from .channel import ChannelBig
    from .coub import BigCoub

    page: int
    per_page: int
    total_pages: int
    coubs: List[BigCoub]
    channels: List[ChannelBig]


class ChannelSearchResponse(BaseModel):
    from .channel import ChannelBig

    page: int
    per_page: int
    total_pages: int
    channels: List[ChannelBig]


class CoubSearchResponse(BaseModel):
    from .coub import BigCoub

    page: int
    per_page: int
    total_pages: int
    coubs: List[BigCoub]
