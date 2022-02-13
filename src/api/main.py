"""Contains the entry point for API."""
import fastapi
from fastapi.responses import JSONResponse

from .schemas import ApplicationData, ResponseData

router = fastapi.APIRouter()


@router.post("/predict", status_code=200, response_model=ResponseData)
async def predict(
    request_data,
) -> fastapi.responses.Response:
    """Predict probability of default for a loan application."""

    prediction = dict()
    response = PredictionPresentor(prediction)

    return response


class PredictionPresentor:
    """Class to prepare a response."""

    @classmethod
    def generate_reponse(cls, data_dict: dict) -> dict:
        """Generate and format a response to send back."""
        default = data_dict.get("prob")
        response_data = {"default": default}
        return JSONResponse(content=response_data)
