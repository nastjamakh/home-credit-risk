"""Contains the Schemas for various messages."""
from pydantic import BaseModel, validator


class ApplicationData(BaseModel):
    """Request schema."""

    sk_id_curr: int

    @validator("city_name")
    def check_value(cls, value: int) -> int:
        """Verify city is supported."""
        return value

    class Config:
        """Request config."""

        schema_extra = {
            "example": {
                "sk_id_curr": 387686,
            }
        }


class ResponseData(BaseModel):
    """Response schema."""

    sk_id_curr: int

    class Config:
        """Response config."""

        schema_extra = {
            "example": {
                "sk_id_curr": 387686,
            }
        }
