from typing import Optional, Annotated

from fastapi import Query
from pydantic import BaseModel


class Hotel(BaseModel):
    id: int
    title: str
    rooms: Optional[int] = None
    location: Optional[str] = None
    created_at: Optional[str] = None

    class Config:
        from_attributes = True


class HotelCreate(BaseModel):
    title: str
    rooms: Optional[int] = None
    location: Optional[str] = None


class HotelUpdate(BaseModel):
    title: Optional[str] = None
    rooms: Optional[int] = None
    location: Optional[str] = None


class HotelsQuery(BaseModel):
    title: Optional[str] = None
    location: Optional[str] = None
    rooms: Optional[int] = None
    page: Annotated[Optional[int], Query(default=1, gt=0)]
    page_size: Annotated[Optional[int], Query(default=5, gt=0, le=30)]


hotels = [
    Hotel(id=1, title="Hotel 1", rooms=3),
    Hotel(id=2, title="Hotel 2", rooms=4),
    Hotel(id=3, title="Hotel 3", rooms=5),
    Hotel(id=4, title="Hotel 4", rooms=6),
    Hotel(id=5, title="Hotel 5", rooms=7),
    Hotel(id=6, title="Hotel 6", rooms=8),
    Hotel(id=7, title="Hotel 7", rooms=9),
    Hotel(id=8, title="Hotel 8", rooms=10),
    Hotel(id=9, title="Hotel 9", rooms=11),
]