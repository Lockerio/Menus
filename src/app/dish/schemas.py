import re

from fastapi import HTTPException
from pydantic import BaseModel, field_validator


PRICE_MATCH_PATTERN = re.compile(r"^\d+(\.\d{1,2})?$")


class DishCreateUpdate(BaseModel):
    title: str
    description: str
    price: str

    @field_validator("price")
    def validate_price(cls, value):
        if not PRICE_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Wrong price value, should be string"
            )
        return value
