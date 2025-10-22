from sqlalchemy import select

from models import HotelsTable
from repositories.base import BaseRepository


class HotelsRepository(BaseRepository):
    model = HotelsTable

    async def get_all(self, queries):
        query = select(self.model).order_by(self.model.id)
        if queries.title:
            query = query.filter(self.model.title.icontains(queries.title))
        if queries.location:
            query = query.filter(self.model.location.icontains(queries.location))
        if queries.rooms:
            query = query.filter(self.model.rooms >= queries.rooms)
        query = (
            query
            .limit(queries.page_size)
            .offset((queries.page - 1) * queries.page_size)
        )
        result = await self.session.execute(query)
        return result.scalars().all()
