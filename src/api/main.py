"""Contains the entry point for API."""
import os
import time
import fastapi
from fastapi.responses import JSONResponse
from modelling.estimator import NaiveEstimator
import pandas as pd

import src.config as config
from .schemas import ApplicationData, ResponseData, ApplicationSingle
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

    pipe.predict(request_data.applications)
    response = pipe.generate_reponse()

    return response


class PredictionPipeline:
    def __init__(self) -> None:
        """Initialize."""
        self.model = NaiveEstimator().load()
        print(f"Loaded model: {self.model}")

    def predict(self, applications_data: list[ApplicationSingle]) -> dict:
        """Predict for goven applications data."""
        X = pd.DataFrame(applications_data)
        X = ApplicationFeatures(flow="predict").generate(df=X)

        idx = pd.Series([app.get("sk_id_curr") for app in applications_data])
        self.preds_ = pd.DataFrame({"sk_id_curr": idx, "target": self.model.predict(X)})
        return self.preds_

    def generate_reponse(self) -> dict:
        """Generate and format a response to send back."""
        response_data = {"predictions": self.preds_.to_dict("records")}
        return JSONResponse(content=response_data)
