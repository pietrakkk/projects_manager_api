from datetime import datetime

from fastapi import HTTPException


def validate_date(date_str: str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid date format for {date_str}. Expected YYYY-MM-DD.")
