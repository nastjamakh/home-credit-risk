import joblib
from lightgbm import LGBMClassifier
from sklearn.model_selection import cross_val_score
from datetime import datetime
from typing import Optional
import numpy as np
import os

from data.training_data import TrainingData
from data_io import DataLoader
from data.agreggators import ApplicationFeatures, TargetData
from config import model_dir
from logger import logger, time_and_log


class TrainingPipeline:
    @staticmethod
    @time_and_log(False)
    def generate_training_dataset() -> tuple:
        data_io = DataLoader()
        data_io.load_dataset(dataset_name="applications")

        data_generator = TrainingData(
            data_io=data_io,
            target=TargetData,
            app_data=ApplicationFeatures,
            merge_on="sk_id_curr",
        )

        data = data_generator.generate_training_dataset()

        # split into X and y
        X = data.drop("target", axis=1)
        y = data["target"]

        return X, y

    @classmethod
    @time_and_log(False)
    def train(cls, model_path: Optional[str] = None):
        logger.info("Training LGBM classifier.")

        X, y = TrainingPipeline.generate_training_dataset()

        # train
        estimator = LGBMClassifier()
        estimator.fit(X, y)

        # serialize model
        model_path = (
            model_path
            if model_path is not None
            else model_dir() / f"model_{datetime.now()}.joblib"
        )
        if not os.path.exists(model_dir()):
            logger.debug("Creating models folder.")
            os.mkdir(model_dir())
        joblib.dump(estimator, model_path)

    @classmethod
    @time_and_log(False)
    def evaluate(cls, cv: int = 5):
        logger.info("Evaluating LGBM classifier.")
        X, y = TrainingPipeline.generate_training_dataset()

        # train & eval
        estimator = LGBMClassifier()
        scores = cross_val_score(estimator, X, y, cv=cv)
        logger.warning(
            {
                "message": "Cross-validation results",
                "cv_scores": scores,
                "cv_score_mean": np.mean(scores),
            }
        )


if __name__ == "__main__":
    TrainingPipeline.evaluate()
