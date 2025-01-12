from geoalchemy2 import Geometry
from sqlalchemy import Column, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from app.core.db.models.base import BaseDBModel, Base


class AreaOfInterest(Base):
    __tablename__ = "area_of_interest"

    file_name = Column(String(100), nullable=False)
    geometry = Column(Geometry('GEOMETRY'), nullable=False)


class Project(Base):
    __tablename__ = "projects"

    name = Column(String(32), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    Column(String, ForeignKey('area_of_interest.id'), nullable=False)
    description = Column(String(300), nullable=True)

    area_of_interest = relationship("AreaOfInterest", back_populates="projects")
