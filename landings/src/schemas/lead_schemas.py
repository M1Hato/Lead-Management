from pydantic import BaseModel, Field, field_validator
from uuid import UUID


class LeadCreate(BaseModel):
    name: str = Field(..., pattern="^[a-zA-Zа-яА-ЯіІїЇєЄґҐ\s\-]+$",
                      description="The name must not contain numbers")
    phone: str = Field(..., pattern=r"^\+\d{7,15}$",
                       description="The phone number format is: +380000000000")
    country: str = Field(..., min_length=2, max_length=2)
    offer_id: UUID
    affiliate_id: UUID

    @field_validator('country')
    @classmethod
    def validate_country_code(cls, v: str) -> str:
        if len(v) != 2:
            raise ValueError("Country code must be 2 letters")
        return v.upper()