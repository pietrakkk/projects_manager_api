

from app.core.db.config import AsyncSessionLocal


async def db_session():
    async with AsyncSessionLocal() as session:
        yield session
