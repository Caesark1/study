from models import RoomsTable
from repositories.base import BaseRepository


class RoomsRepository(BaseRepository):
    model = RoomsTable
