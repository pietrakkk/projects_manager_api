import uuid

from sqlalchemy import Column, Integer
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql.expression import func
from sqlalchemy.types import DateTime


class BaseDBModel:
    id = Column(Integer, primary_key=True, default=uuid.uuid4)
    created = Column(DateTime, default=func.now(), nullable=False)
    modified = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)


Base = declarative_base(cls=BaseDBModel)
