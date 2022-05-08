from typing import Optional, Tuple

import fire
import numpy as np
from sklearn.model_selection import cross_val_score
import pandas as pd

from data.agreggators import ApplicationFeatures, TargetData
from data.training_data import TrainingData
from data_loader import DataLoader
from logger import logger, time_and_log
from modelling.estimator import HomeCreditEstimator

CV_SCORING_METRIC = "recall"


class TrainingPipeline:
    """Training pipeline."""

    @staticmethod
    @time_and_log(False, "INFO")
    def generate_training_dataset() -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Create training dataset."""
        data_io = DataLoader()
        data_io.load_dataset(dataset_name="applications")

        data_generator = TrainingData(
            data_io=data_io,
            target=TargetData,
            features=[ApplicationFeatures],
            merge_on="sk_id_curr",
        )

        data = data_generator.generate_training_dataset()

        # split into X and y
        X = data.drop("target", axis=1)
        y = data["target"]

        return X, y

    @classmethod
    @time_and_log(False)
    def train(cls, to_s3: Optional[bool] = False) -> None:
        """Train."""
        logger.warning(f"Training LGBM classifier. TO S3: {to_s3}")

        X, y = TrainingPipeline.generate_training_dataset()

        # train
        estimator = HomeCreditEstimator()
        estimator.fit(X, y)

        # serialize model
        estimator.save(to_s3=to_s3)

    def load_model(self) -> None:
        estimator = HomeCreditEstimator()
        estimator.load(from_s3=True)

    @classmethod
    @time_and_log(False)
    def evaluate(cls, cv: int = 5, scoring: str = CV_SCORING_METRIC) -> None:
        """Evaluate."""
        logger.info("Evaluating LGBM classifier.")
        X, y = TrainingPipeline.generate_training_dataset()

        # train & eval
        estimator = HomeCreditEstimator()
        scores = cross_val_score(estimator.model, X, y, cv=cv, scoring=scoring)
        logger.warning(
            {
                "message": "Cross-validation results",
                "metric": scoring,
                "cv_scores": scores,
                "cv_score_mean": np.mean(scores),
            }
        )


def cli() -> None:
    """CLI interface for training and evaluation."""
    fire.Fire(TrainingPipeline)


if __name__ == "__main__":
    cli()
