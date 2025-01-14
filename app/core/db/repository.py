from typing import Any, Dict, Generic, List, Type, TypeVar

from core.db.config import AsyncSessionLocal
from core.db.models import Base
from sqlalchemy import delete, select, update
from sqlalchemy.exc import NoResultFound

T = TypeVar("T", bound=Base)


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
            entity = await session.get(self.db_model, entity_id)

            if not entity:
                raise NoResultFound("Cannot find item")

            return entity

    async def list(self) -> List[T]:
        async with self.session_factory() as session:
            result = await session.execute(select(self.db_model))
            return [i for i in result.scalars().all() if i]

    async def remove(self, entity_id: str) -> None:
        async with self.session_factory() as session:
            await self.get_by_id(entity_id)

            stmt = delete(self.db_model).where(self.db_model.id == entity_id)
            await session.execute(stmt)
            return await session.commit()

    async def update(self, entity_id: int, update_data: Dict[str, Any]) -> T:
        async with self.session_factory() as session:
            stmt = (
                update(self.db_model)
                .where(self.db_model.id == entity_id)
                .values(**update_data)
                .execution_options(synchronize_session="fetch")
            )
            await session.execute(stmt)
            await session.commit()

            return await self.get_by_id(entity_id)
