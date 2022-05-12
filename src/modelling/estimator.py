"""Final estimator."""
from datetime import datetime
from typing import Any, Sized
import numpy as np

import fire
import serialization.utils as utils
from config import model_dir
from lightgbm import LGBMClassifier
from logger import time_and_log
from serialization.serializers import Serializer


class HeuristicEstimator:
    """Wrapper for LightGBM estimator."""

    def __init__(self) -> None:
        """Initialize."""
        self.model = LGBMClassifier()

    def fit(self, *args: Any, **kwargs: Any) -> None:
        """Wrapper around model fit method."""
        pass

    def predict(self, X: Sized) -> list:
        return self.run_rules(X)

    def run_rules(self, X: Sized) -> list:
        return np.multiply(self.rule_1(X), self.rule_2(X))

    def rule_1(self, X: Sized) -> list:
        return [1] * len(X)

    def rule_2(self, X: Sized) -> list:
        return [0] * len(X)

    @time_and_log(False)
    def save(self, to_s3: bool = False) -> None:
        """Serialize the model."""
        model_path = (
            model_dir()
            / f"model_{datetime.now().strftime(utils.DATETIME_FORMAT)}.joblib"
        )
        Serializer().write(file_id=model_path, object=self.model, to_s3=to_s3)

    @time_and_log(False)
    def load(self, from_s3: bool = False) -> Any:
        """Download model from S3."""
        # Load from local file
        Serializer().read(file_type="model", from_s3=from_s3)


class HomeCreditEstimator:
    """Wrapper for LightGBM estimator."""

    def __init__(self) -> None:
        """Initialize."""
        self.model = LGBMClassifier()

    def fit(self, *args: Any, **kwargs: Any) -> None:
        """Wrapper around model fit method."""
        self.model.fit(*args, **kwargs)

    def select_hyperparameters(self) -> None:
        """Perform automatic hyperparaemter tuning and save best version."""
        raise NotImplementedError

    @time_and_log(False)
    def save(self, to_s3: bool = False) -> None:
        """Serialize the model."""
        model_path = (
            model_dir()
            / f"model_{datetime.now().strftime(utils.DATETIME_FORMAT)}.joblib"
        )
        Serializer().write(file_id=model_path, object=self.model, to_s3=to_s3)

    @time_and_log(False)
    def load(self, from_s3: bool = False) -> Any:
        """Download model from S3."""
        # Load from local file
        Serializer().read(file_type="model", from_s3=from_s3)


def cli() -> None:
    """CLI interface for training and evaluation."""
    fire.Fire(HomeCreditEstimator)


if __name__ == "__main__":
    cli()
