from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.settings import Settings

engine = create_async_engine(str(Settings.db_url), echo=Settings.db_echo, plugins=["geoalchemy2"])

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
