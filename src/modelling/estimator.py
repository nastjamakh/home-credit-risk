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


class NaiveEstimator(BaseEstimator):
    """Estimator that predicts an average probability of default given column bins."""

    MAX_BINS = 20

    @classmethod
    def name(cls) -> str:
        return "naive_estimator"

    def __init__(self, margin: int = 0):
        self.bins_dict: dict = dict()
        self.bins_map: dict = dict()
        self.cat_map: dict = dict()
        self.margin: int = margin

        self.is_fit = False

    @staticmethod
    def get_numeric_columns(df: pd.DataFrame) -> pd.DataFrame:
        """Get a subset of data only with numeric columns."""
        return df.select_dtypes("number")

    @staticmethod
    def get_categorical_columns(df: pd.DataFrame) -> pd.DataFrame:
        """Get a subset of data only with categorical columns."""
        return df.select_dtypes(object)

    def fit(self, X: pd.DataFrame, y: pd.Series) -> None:
        """Create bins for all numeric columns and save default rate for each bin."""
        df = X.copy()
        df["target"] = y

        # create bins for numeric features and save default rate
        for col in NaiveEstimator.get_numeric_columns(X).columns:
            # use 20 bins if number of unique valeus exceeds 20
            q = min(self.MAX_BINS, X[col].nunique())

            # apply and save qcut bins
            binned, bins_ = pd.qcut(
                X[col], q, duplicates="drop", retbins=True, labels=False
            )

            self.bins_dict[col] = bins_
            self.bins_map[col] = df.groupby(binned).target.mean()

        # save default rate for categorical features
        for col in NaiveEstimator.get_categorical_columns(X).columns:
            self.cat_map[col] = df.groupby(col).mean().target

        self.default_avg_ = y.mean()
        self.is_fit = True

    def predict_proba(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Get average default rate for each column.

        Return average of all columns.
        """
        X_copy = X.copy().drop("sk_id_curr", axis=1)
        for col in NaiveEstimator.get_numeric_columns(X_copy).columns:
            X_copy[col] = (
                pd.cut(
                    X_copy[col],
                    bins=self.bins_dict[col],
                    labels=False,
                    include_lowest=True,
                )
                .map(self.bins_map[col])
                .fillna(self.default_avg_)
            )
        for col in NaiveEstimator.get_categorical_columns(X_copy).columns:
            X_copy[col] = X_copy[col].map(self.cat_map[col]).fillna(self.default_avg_)

        # mean
        prob_default = X_copy.mean(1)

        return prob_default

    def predict(self, X: pd.DataFrame) -> pd.DataFrame:
        """Return 1 if expect default, 0 otherwise."""

        probs = self.predict_proba(X)
        default = (probs > self.default_avg_ * (1 + self.margin / 100)).astype(int)
        return default

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

    @staticmethod
    @time_and_log(False)
    def load(from_s3: bool = False) -> Any:
        """Download model from S3."""
        # Load from local file
        return Serializer().read(file_type="model", from_s3=from_s3)


def cli() -> None:
    """CLI interface for training and evaluation."""
    fire.Fire(NaiveEstimator)


if __name__ == "__main__":
    cli()
