import asyncio
import threading
import time
from typing import Any, Annotated, Optional

from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Depends, Body
from sqlalchemy import insert, select

from database import async_session_maker
from models.hotels import HotelsTable
from repositories.hotels import HotelsRepository
from src.schemas.schemas import hotels, Hotel, HotelsQuery, HotelCreate, HotelUpdate

hotel_routers = APIRouter(prefix="/api/hotels", tags=["Hotels"])


# @hotel_routers.get("/sync/{id}")
# def sync_get(id: int) -> dict[str, Any]:
#     print(f"SYNC THREADING: {threading.active_count()}")
#     print(f"SYNC START: {time.time():.2f} {id}")
#     time.sleep(3)
#     print(f"SYNC END: {time.time():.2f} {id}")
#     return {"message": f"Hello from sync endpoint with id {id}"}
#
#
# @hotel_routers.get("/async/{id}")
# async def async_get(id: int) -> dict[str, Any]:
#     print(f"ASYNC THREADING: {threading.active_count()}")
#     print(f"ASYNC START: {time.time():.2f}")
#     await asyncio.sleep(3)
#     print(f"ASYNC END: {time.time():.2f}")
#     return {"message": f"Hello from sync endpoint with id {id}"}


@hotel_routers.get("/")
async def get_hotels(
        queries: Annotated[HotelsQuery, Depends()] = None,
) -> list[Hotel]:
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(queries)


@hotel_routers.get("/{hotel_id}")
async def get_hotel(hotel_id: int) -> Hotel | dict[str, Any]:
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).get_one_or_none(id=hotel_id)
        if hotel:
            return Hotel.model_validate(hotel)
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
        hotel = await HotelsRepository(session).create(**hotel.model_dump())
        await session.commit()
        await session.refresh(hotel)
        print(hotel.id)
        return {"status": "OK", "hotel": Hotel.model_validate(hotel)}


@hotel_routers.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int) -> dict[str, Any]:
    async with async_session_maker() as session:
        result = await HotelsRepository(session).delete_one(id=hotel_id)
        if result:
            await session.delete(result)
            await session.commit()
            return {"status": "OK"}
    return {"error": "Hotel not found"}


@hotel_routers.put(
    "/{hotel_id}",
)
async def update_hotel(hotel_id: int, hotel: HotelUpdate) -> Hotel | dict[str, Any]:
    async with async_session_maker() as session:
        result = await HotelsRepository(session).update(
            hotel.model_dump(), hotel_id=hotel_id
        )
        await session.commit()
        if result:
            return Hotel.model_validate(result)
        return {"error": "Hotel not found"}


@hotel_routers.patch("/{hotel_id}")
def partial_update_hotel(hotel_id: int, hotel: Hotel) -> Hotel:
    stored_hotel_encoded = jsonable_encoder(hotels[hotel_id])
    stored_item_model = Hotel(**stored_hotel_encoded)
    update_data = hotel.model_dump(exclude_unset=True)
    updated_item = stored_item_model.model_copy(update=update_data)
    hotels[hotel_id] = jsonable_encoder(updated_item)
    return updated_item
