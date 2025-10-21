import asyncio
import threading
import time
from typing import Any, Annotated

from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Depends, Body
from sqlalchemy import insert, select

from database import async_session_maker
from models.hotels import HotelsTable
from src.schemas.schemas import hotels, Hotel, HotelsQuery, HotelCreate

hotel_routers = APIRouter(prefix="/api/hotels", tags=["Hotels"])


@hotel_routers.get("/sync/{id}")
def sync_get(id: int) -> dict[str, Any]:
    print(f"SYNC THREADING: {threading.active_count()}")
    print(f"SYNC START: {time.time():.2f} {id}")
    time.sleep(3)
    print(f"SYNC END: {time.time():.2f} {id}")
    return {"message": f"Hello from sync endpoint with id {id}"}


@hotel_routers.get("/async/{id}")
async def async_get(id: int) -> dict[str, Any]:
    print(f"ASYNC THREADING: {threading.active_count()}")
    print(f"ASYNC START: {time.time():.2f}")
    await asyncio.sleep(3)
    print(f"ASYNC END: {time.time():.2f}")
    return {"message": f"Hello from sync endpoint with id {id}"}


@hotel_routers.get("/")
async def get_hotels(
        queries: Annotated[HotelsQuery, Depends()] = None,
) -> list[Hotel]:
    async with async_session_maker() as session:
        query = select(HotelsTable)
        if queries.title:
            query = query.filter(HotelsTable.title.ilike(f"%{queries.title}%"))
        if queries.location:
            query = query.filter(HotelsTable.location.ilike(f"%{queries.location}%"))
        if queries.rooms:
            query = query.filter(HotelsTable.rooms >= queries.rooms)
        query = (
            query
            .limit(queries.page_size)
            .offset((queries.page - 1) * queries.page_size)
        )
        result = await session.execute(query)

    # data = hotels
    # if queries.title:
    #     data = [
    #         hotel for hotel in hotels if queries.title.lower() in hotel.title.lower()
    #     ]
    #
    # start = (queries.page - 1) * queries.page_size
    # end = start + queries.page_size
    return result.scalars().all()


@hotel_routers.get("/{hotel_id}")
def get_hotel(hotel_id: int) -> Hotel | dict[str, Any]:
    for hotel in hotels:
        if hotel.id == hotel_id:
            return hotel
    return {"error": "Hotel not found"}


@hotel_routers.post("/")
async def create_hotel(
        hotel: HotelCreate = Body(
            openapi_examples={
                "1": {
                    "summary": "Тест со всеми данными",
                    "value": {
                        "title": "Test Hotel",
                        "rooms": 3,
                        "location": "Test Location",
                    },
                },
                "2": {
                    "summary": "Тест только с именем",
                    "value": {
                        "title": "Test Hotel",
                    }
                }
            }
        )
) -> dict:
    async with async_session_maker() as session:
        add_hotel_stmt = insert(HotelsTable).values(
            **hotel.model_dump()
        )
        await session.execute(add_hotel_stmt)
        await session.commit()
        # session.add(hotel)
        # await session.commit()
        # await session.refresh(hotel)
    return {"hotel": "TEST"}


@hotel_routers.delete("/{hotel_id}")
def delete_hotel(hotel_id: int) -> dict[str, Any]:
    for hotel in hotels:
        if hotel.id == hotel_id:
            hotels.remove(hotel)
            return {"message": "Hotel deleted"}
    return {"error": "Hotel not found"}


@hotel_routers.put(
    "/{hotel_id}",
    response_model=Hotel,
    responses={404: {"description": "Hotel not found"}},
)
def update_hotel(hotel_id: int, hotel: Hotel) -> Hotel:
    update_hotel_encoded = jsonable_encoder(hotel)
    hotels[hotel_id] = update_hotel_encoded
    return hotel


@hotel_routers.patch("/{hotel_id}")
def partial_update_hotel(hotel_id: int, hotel: Hotel) -> Hotel:
    stored_hotel_encoded = jsonable_encoder(hotels[hotel_id])
    stored_item_model = Hotel(**stored_hotel_encoded)
    update_data = hotel.model_dump(exclude_unset=True)
    updated_item = stored_item_model.model_copy(update=update_data)
    hotels[hotel_id] = jsonable_encoder(updated_item)
    return updated_item
