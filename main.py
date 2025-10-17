from typing import Any, Annotated

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.params import Query
from pydantic import BaseModel

app = FastAPI()


class Hotel(BaseModel):
    id: int
    title: str


hotels = [
    Hotel(id=1, title="Hotel 1"),
    Hotel(id=2, title="Hotel 2"),
    Hotel(id=3, title="Hotel 3"),
]


@app.get("/hotels")
def get_hotels(title: Annotated[str, Query(description="Filter hotels by title")] = None) -> list[Hotel]:
    if title:
        return [hotel for hotel in hotels if title.lower() in hotel.title.lower()]
    return hotels


@app.get("/hotels/{hotel_id}")
def get_hotel(hotel_id: int) -> Hotel | dict[str, Any]:
    for hotel in hotels:
        if hotel.id == hotel_id:
            return hotel
    return {"error": "Hotel not found"}


@app.post("/hotels")
def create_hotel(hotel: Hotel) -> Hotel:
    hotels.append(hotel)
    return hotel


@app.delete("/hotels/{hotel_id}")
def delete_hotel(hotel_id: int) -> dict[str, Any]:
    for hotel in hotels:
        if hotel.id == hotel_id:
            hotels.remove(hotel)
            return {"message": "Hotel deleted"}
    return {"error": "Hotel not found"}


@app.put(
    "/hotels/{hotel_id}",
    response_model=Hotel,
    responses={404: {"description": "Hotel not found"}},
)
def update_hotel(hotel_id: int, hotel: Hotel) -> Hotel:
    update_hotel_encoded = jsonable_encoder(hotel)
    hotels[hotel_id] = update_hotel_encoded
    return hotel


@app.patch("/hotels/{hotel_id}")
def partial_update_hotel(hotel_id: int, hotel: Hotel) -> Hotel:
    stored_hotel_encoded = jsonable_encoder(hotels[hotel_id])
    stored_item_model = Hotel(**stored_hotel_encoded)
    update_data = hotel.model_dump(exclude_unset=True)
    updated_item = stored_item_model.model_copy(update=update_data)
    hotels[hotel_id] = jsonable_encoder(updated_item)
    return updated_item


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
