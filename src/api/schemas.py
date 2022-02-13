"""Contains the Schemas for various messages."""
from pydantic import BaseModel, validator
from typing import List

from logger import logger


class ApplicationData(BaseModel):
    """Request schema."""

    lookahead: int

    @validator("lookahead")
    def valid_lookahead(cls, lookahead: int) -> int:
        """Verify lookahead is a positive integer."""
        if lookahead <= 0:
            logger.warning(
                {
                    "process": "valid_lookahead",
                    "message": "Lookahead must be positive",
                    "lookahead": lookahead,
                }
            )
            raise ValueError("Lookahead must be positve")
        elif not isinstance(lookahead, int):
            logger.warning(
                {
                    "process": "valid_lookahead",
                    "message": "Lookahead must be an integer",
                    "lookahead": lookahead,
                }
            )
            raise ValueError("Lookahead must be an integer")
        return lookahead

    class Config:
        """Request config."""

        schema_extra = {
            "example": {
                "city_name": "HAMBURG",
                "predict_from": "2020-10-2T23:00:00",
                "lookahead": 8,
            }
        }


class DropOffPoint(BaseModel):
    """Drop-Off Point schema."""

    id: int
    dynamicCapacity: float
    priority: int

    @validator("dynamicCapacity")
    def valid_priority(cls, value: int) -> int:
        """Verify priority is between 0 and 100."""
        if value not in [0, 25, 50, 100]:
            raise ValueError(f"Priority must be one of [0, 25, 50, 100], not {value}.")
        return value


class ResponseData(BaseModel):
    """Response schema."""

    zoneID: str
    dropOffPoints: List[DropOffPoint]

    class Config:
        """Response config."""

        schema_extra = {
            "example": {
                "zoneID": "BONN",
                "dropOffPoints": [
                    {"id": 5860, "dynamic_capacity": 3.0, "priority": 25}
                ],
            }
        }
