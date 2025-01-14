import datetime
from enum import Enum
from typing import Any

from core.utils import validate_date
from pydantic import BaseModel, Field, model_validator


class GeoJsonfileType(Enum):
    feature = "Feature"


class ProjectCreate(BaseModel):
    name: str = Field(..., max_length=32)
    start_date: datetime.date
    end_date: datetime.date
    description: str | None = Field(..., max_length=255)

    @model_validator(mode="before")
    @classmethod
    def validate_dates(cls, data: dict[str, Any]) -> dict[str, Any]:
        date_range_start = validate_date(data.get("start_date"))
        date_range_end = validate_date(data.get("end_date"))

        if date_range_end < date_range_start:
            raise ValueError("End date must be after start date.")

        return data


class ProjectListResponse(BaseModel):
    id: str
    name: str
    start_date: datetime.date
    end_date: datetime.date
    description: str | None
    created: datetime.datetime
    modified: datetime.datetime


class ProjectUpdate(BaseModel):
    name: str
    description: str | None
