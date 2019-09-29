from typing import List, Optional

from pydantic import BaseModel

from .coub import BigCoub

__all__ = ("SectionTimeLineResponse", "TimeLineResponse", "MyTimeLineResponse")


class SectionTimeLineResponse(BaseModel):
    page: int
    per_page: int
    total_pages: int
    next: Optional[float]
    coubs: List[BigCoub]


class TimeLineResponse(BaseModel):
    page: int
    per_page: int
    total_pages: int
    coubs: List[BigCoub]


class MyTimeLineResponse(BaseModel):
    page: int
    per_page: int
    total_pages: int
    coubs: List[dict]  # TODO
