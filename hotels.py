import asyncio
import threading
import time
from typing import Any, Annotated

from fastapi.encoders import jsonable_encoder
from fastapi import Query, APIRouter

from schemas import hotels, Hotel, HotelsQuery

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
def get_hotels(
        queries: Annotated[HotelsQuery, Query()] = None,
) -> list[Hotel]:
    data = hotels
    if queries.title:
        data = [
            hotel for hotel in hotels if queries.title.lower() in hotel.title.lower()
        ]

    start = (queries.page - 1) * queries.page_size
    end = start + queries.page_size
    return data[start:end]


@hotel_routers.get("/{hotel_id}")
def get_hotel(hotel_id: int) -> Hotel | dict[str, Any]:
    for hotel in hotels:
        if hotel.id == hotel_id:
            return hotel
    return {"error": "Hotel not found"}


@hotel_routers.post("/")
def create_hotel(hotel: Hotel) -> Hotel:
    hotels.append(hotel)
    return hotel


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
