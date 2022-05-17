"""Contains the entry point for API."""
import os
import time
import fastapi
from fastapi.responses import JSONResponse
from modelling.estimator import NaiveEstimator
import pandas as pd

import src.config as config
from .schemas import ApplicationData, ResponseData
from data.features import ApplicationFeatures

# Setup timezone info
os.environ["TZ"] = config.TIMEZONE
time.tzset()

router = fastapi.APIRouter()


@router.post("/predict", status_code=200, response_model=ResponseData)
async def predict_default(
    request_data: ApplicationData,
) -> fastapi.responses.Response:
    """Predict default probability for an application."""
    pipe = PredictionPipeline()
    pred = pipe.predict(dict(request_data))

    return PredictionsPresentor.generate_reponse(
        sk_id_curr=request_data.sk_id_curr, pred=pred
    )


class PredictionsPresentor:
    """Class to prepare a response."""

    @classmethod
    def generate_reponse(cls, sk_id_curr: int, pred: dict) -> dict:
        """Generate and format a response to send back."""
        response_data = {"sk_id_curr": sk_id_curr, "pred": pred}
        print(response_data)
        return JSONResponse(content=response_data)


class PredictionPipeline:
    def __init__(self) -> None:
        self.model = NaiveEstimator().load()
        print(f"Loaded model: {self.model}")

    def predict(self, request_data: dict) -> dict:
        X = pd.DataFrame.from_dict(request_data, orient="index").T
        X = ApplicationFeatures(flow="predict").generate(df=X)
        return self.model.predict(X)
