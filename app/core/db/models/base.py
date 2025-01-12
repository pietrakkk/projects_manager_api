import uuid

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql.expression import func
from sqlalchemy.types import DateTime


class BaseDBModel:
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created = Column(DateTime, default=func.now(), nullable=False)
    modified = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)


Base = declarative_base(cls=BaseDBModel)
