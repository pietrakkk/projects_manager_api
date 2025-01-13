from typing import Generic, TypeVar, List, Type

from sqlalchemy import select

from core.db.config import AsyncSessionLocal
from core.db.models import Base

T = TypeVar('T', bound=Base)


class DBRepository(Generic[T]):
    db_model: Type[T] = None

    def __init__(self, session_factory=AsyncSessionLocal):
        self.session_factory = session_factory

    async def add(self, entity: T) -> T:
        async with self.session_factory() as session:
            session.add(entity)
            await session.commit()
            return entity

    async def get_by_id(self, entity_id: int) -> T:
        async with self.session_factory() as session:
            return await session.get(self.db_model, entity_id)

    async def list(self) -> List[T]:
        async with self.session_factory() as session:
            result = await session.execute(select(self.db_model))
            return [i for i in result.scalars().all() if i]

    async def remove(self, entity: T) -> None:
        async with self.session_factory() as session:
            await session.delete(entity)
            await session.commit()
