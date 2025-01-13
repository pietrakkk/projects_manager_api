import uuid

from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql.expression import func
from sqlalchemy.types import DateTime


class BaseDBModel:
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created = Column(DateTime, default=func.now(), nullable=False)
    modified = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)


Base = declarative_base(cls=BaseDBModel)
