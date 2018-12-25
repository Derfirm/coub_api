from typing import List

from pydantic import BaseModel

from .coub import BigCoub

__all__ = ("SectionTimeLineResponse", "TimeLineResponse")


class SectionTimeLineResponse(BaseModel):
    page: int
    per_page: int
    total_pages: int
    next: float
    coubs: List[BigCoub]


class TimeLineResponse(BaseModel):
    page: int
    per_page: int
    total_pages: int
    coubs: List[BigCoub]
