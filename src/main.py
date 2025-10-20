import sys

from pathlib import Path

from fastapi import FastAPI

sys.path.append(str(Path(__file__).parent.parent))

from src.api.hotels import hotel_routers
from src.database import *

app = FastAPI()

app.include_router(hotel_routers)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
