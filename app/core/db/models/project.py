from core.db.models.base import Base
from geoalchemy2 import Geometry
from sqlalchemy import Column, Date, ForeignKey, String
from sqlalchemy.orm import relationship


class AreaOfInterest(Base):
    __tablename__ = "area_of_interest"

    file_name = Column(String(100), nullable=False)
    geometry = Column(Geometry("GEOMETRY", nullable=False))
    project_id = Column(String, ForeignKey("projects.id", ondelete="CASCADE"))
    project = relationship("Project", back_populates="area_of_interest")


class Project(Base):
    __tablename__ = "projects"

    name = Column(String(32), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    description = Column(String(255), nullable=True)

    area_of_interest = relationship(
        "AreaOfInterest",
        uselist=False,
        back_populates="project",
        cascade="all, delete-orphan",
    )
