"""Final estimator."""
from datetime import datetime
from typing import Any

import fire
import serialization.utils as utils
from config import model_dir
from lightgbm import LGBMClassifier
from logger import time_and_log
from serialization.serialization import Serializer


class HomeCreditEstimator:
    """Wrapper for LightGBM estimator."""

    def __init__(self) -> None:
        """Initialize."""
        self.model = LGBMClassifier()

    def fit(self, *args: Any, **kwargs: Any) -> None:
        """Wrapper around model fit method."""
        self.model.fit(*args, **kwargs)

    def select_hyperparameters(self):
        """Perform automatic hyperparaemter tuning and save best version."""
        raise NotImplementedError

    @time_and_log(False)
    def save(self, to_s3: bool = False) -> None:
        """Serialize the model."""
        model_path = (
            model_dir()
            / f"model_{datetime.now().strftime(utils.DATETIME_FORMAT)}.joblib"
        )
        Serializer(file_id=model_path).write(object=self.model, to_s3=to_s3)

    @time_and_log(False)
    def load(self, latest: bool = True, from_s3: bool = False):
        """Download model from S3."""
        # Load from local file
        Serializer(latest=True).write(from_s3=from_s3)


def cli():
    """CLI interface for training and evaluation."""
    fire.Fire(HomeCreditEstimator)


if __name__ == "__main__":
    cli()
