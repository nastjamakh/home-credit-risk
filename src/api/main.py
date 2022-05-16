"""Contains the entry point for API."""
import os
import time
import fastapi
from fastapi.responses import JSONResponse

import src.config as config

from .schemas import ApplicationData, ResponseData

# Setup timezone info
os.environ["TZ"] = config.TIMEZONE
time.tzset()

router = fastapi.APIRouter()


@router.post("/predict", status_code=200, response_model=ResponseData)
async def predict_default(
    request_data: ApplicationData,
) -> fastapi.responses.Response:
    """Predict default probability for an application."""
    pass


class PredictionsPresentor:
    """Class to prepare a response."""

    @classmethod
    def generate_reponse(cls, sk_id_curr: int) -> dict:
        """Generate and format a response to send back."""
        response_data = {"sk_id_curr": sk_id_curr}
        return JSONResponse(content=response_data)
