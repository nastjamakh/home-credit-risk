"""Final estimator."""
import os
from datetime import datetime
from typing import Any

import fire
import joblib
from config import aws_s3_bucket_name, model_dir
from lightgbm import LGBMClassifier
from logger import logger, time_and_log
from s3 import S3Handler, _FileId
import modelling.utils as utils


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
    def serialize(self, to_s3: bool = False) -> None:
        """Serialize the model."""
        model_path = (
            model_dir()
            / f"model_{datetime.now().strftime(utils.DATETIME_FORMAT)}.joblib"
        )
        if not os.path.exists(model_dir()):
            logger.debug("Creating models folder.")
            os.mkdir(model_dir())
        joblib.dump(self.model, model_path)

        if to_s3:
            if aws_s3_bucket_name():
                file_id = _FileId(model_path)
                S3Handler(file_id).upload()
                logger.info("Upload to s3: Success.")
            else:
                logger.warning("NO AWS S3 BUCKET NAME PROVIDED. Skipping.")

    @time_and_log(False)
    def from_file(self, latest: bool = True, from_s3: bool = False):
        """Download model from S3."""
        # Load from local file
        if not from_s3:
            if os.path.exists(model_dir()) and len(os.listdir(model_dir())) > 0:
                model_filename = utils.get_latest_model_file_id()
                model = joblib.load(model_filename)
                return model
            else:
                raise FileExistsError("No model files found.")
        # Load from S3
        else:

            if aws_s3_bucket_name():
                model = "model_2022-05-05 22:35:12.867349.joblib"
                file_id = _FileId(model_dir() / model)
                S3Handler(file_id).download()
                logger.info("Upload to s3: Success.")
            else:
                logger.warning("NO AWS S3 BUCKET NAME PROVIDED. Skipping.")


def cli():
    """CLI interface for training and evaluation."""
    fire.Fire(HomeCreditEstimator)


if __name__ == "__main__":
    cli()
