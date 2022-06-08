"""Final estimator."""
from datetime import datetime
from typing import Any
import pandas as pd

import fire
import serialization.utils as utils
from config import model_dir
from logger import time_and_log
from serialization.serializers import Serializer
from sklearn.base import BaseEstimator

DEFAULT_THRESH = 0.081


class NaiveEstimator(BaseEstimator):
    """Estimator that predicts an average probability of default given column bins."""

    DROP_COLS = ["sk_id_curr"]
    MAX_BINS = 20

    @classmethod
    def name(cls) -> str:
        return "naive_estimator"

    def __init__(self, margin: float = 0):
        self.bins_dict: dict = dict()
        self.bins_map: dict = dict()

        self.margin = 0
        self.is_fit = False

    @staticmethod
    def get_numeric_columns(df: pd.DataFrame) -> pd.DataFrame:
        """Get a subset of data only with numeric columns."""
        return df.select_dtypes("number").drop(NaiveEstimator.DROP_COLS, axis=1)

    def fit(self, X: pd.DataFrame, y: pd.Series) -> None:
        """Create bins for all numeric columns and save default rate for each bin."""
        df = X.copy()
        df["target"] = y

        for col in NaiveEstimator.get_numeric_columns(X).columns:
            # use 20 bins if number of unique valeus exceeds 20
            q = min(self.MAX_BINS, X[col].nunique())

            # apply and save qcut bins
            binned, bins_ = pd.qcut(
                X[col], q, duplicates="drop", retbins=True, labels=False
            )

            self.bins_dict[col] = bins_
            self.bins_map[col] = df.groupby(binned).target.mean()
        self.is_fit = True

    def predict_proba(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Get average default rate for each column.

        Return average of all columns.
        """
        X_copy = X.copy()
        for col in NaiveEstimator.get_numeric_columns(X).columns:
            X_copy[col] = (
                pd.cut(
                    X[col], bins=self.bins_dict[col], labels=False, include_lowest=True
                )
                .map(self.bins_map[col])
                .fillna(DEFAULT_THRESH)
            )

        prob_default = NaiveEstimator.get_numeric_columns(X_copy).mean(1)

        probs = prob_default > DEFAULT_THRESH * (1 + self.margin)
        return probs

    def predict(self, X: pd.DataFrame) -> pd.DataFrame:
        """Return 1 if expect default, 0 otherwise."""

        probs = self.predict_proba(X)
        return probs.astype(int)

    @time_and_log(False)
    def save(self, to_s3: bool = False) -> None:
        """Serialize the model."""
        timestamp = datetime.now().strftime(utils.DATETIME_FORMAT)
        model_path = model_dir() / f"model_{self.name()}_{timestamp}.joblib"
        Serializer().write(file_id=model_path, obj=self, to_s3=to_s3)

    @time_and_log(False)
    def load_from_s3(self) -> None:
        """Download model from S3."""
        # Load from local file
        Serializer().read(file_type="model", from_s3=True)

    @time_and_log(False)
    def load(self, from_s3: bool = False) -> Any:
        """Download model from S3."""
        # Load from local file
        return Serializer().read(file_type="model", from_s3=from_s3)


def cli() -> None:
    """CLI interface for training and evaluation."""
    fire.Fire(NaiveEstimator)


if __name__ == "__main__":
    cli()
