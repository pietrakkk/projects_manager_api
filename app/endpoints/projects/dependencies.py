from endpoints.projects.schema import ProjectCreate
from fastapi import Form, HTTPException
from pydantic import ValidationError
from starlette import status


async def get_form_payload(
    name: str = Form(..., max_length=32),
    start_date: str = Form(
        ...,
    ),
    end_date: str = Form(...),
    description: str | None = Form(None, max_length=255),
) -> ProjectCreate:
    try:
        return ProjectCreate(
            name=name,
            start_date=start_date,
            end_date=end_date,
            description=description,
        )
    except ValidationError as exc:
        errors = [
            {
                "field": ".".join(str(e) for e in error.get("loc")),
                "message": error.get("msg"),
                "type": error.get("type"),
            }
            for error in exc.errors()
        ]

        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=errors
        )
