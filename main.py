from fastapi import FastAPI

from hotels import hotel_routers

app = FastAPI()

app.include_router(hotel_routers)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
