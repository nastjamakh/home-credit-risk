"""
    Responsabilities:
    - (De) Serialization
    - Download/Upload files to and from S3 if they dont exists locally
    - Model-Zoo
"""
import os
from typing import Any, Optional

import config
import joblib
from logger import logger, time_and_log
from serialization.s3 import S3Handler
from serialization.utils import _FileId


class ModelSerializer:
    """object <-> file with joblib"""

    def __init__(
        self, file_id: Optional[_FileId] = None, file_type: Optional[str] = None
    ) -> None:
        """Initialize."""
        assert not (
            file_id is None and file_type is None
        ), "Must specify either file_id (write) or file_type (read)."
        self.file_type = file_type
        self.file_id = file_id

    def read(self) -> None:
        """Load model from file."""
        if self.file_id:
            return joblib.load(self.file_id.to_path())
        else:
            # get latest model file
            model_files = [
                config.model_dir() / mf for mf in os.listdir(config.model_dir())
            ]
            latest = max(model_files, key=lambda fpath: fpath.stat().st_mtime)
            return joblib.load(latest)

    def write(self, obj) -> None:
        """Write model to file."""
        logger.debug(
            {
                "process": "ModelSerializer.write",
                "message": f"serializing file {self.file_id.to_path()}",
            }
        )
        if not os.path.exists(config.model_dir()):
            logger.debug("Creating models folder.")
            os.mkdir(config.model_dir())
        joblib.dump(obj, self.file_id.to_path())


class Serializer:
    """
    Writes object to the disk or on S3 (serialization) and return an
    object from a file (de-serialization).

    Serialization:
    - Writes the file on the disk on development
    - Writes on S3 if force_s3 is enabled
    - Write on S3 on production

    De-serialization:
    - If the file can not be found on the disk, it will retrieve it from S3
    - If it can not be found on S3, it will raise an Error
    """

    @staticmethod
    def get_correct_serializer(
        file_id: Optional[_FileId] = None, file_type: Optional[str] = None
    ):
        assert not (
            file_id is None and file_type is None
        ), "Must specify either file_id (write) or file_type (read)."
        if file_id:
            file_path = file_id.to_path()

            if file_path.suffix == ".joblib":
                return ModelSerializer(file_id=file_id)
            else:
                raise ValueError("{} not supported".format(file_path.suffix))
        else:
            if file_type == "model":
                return ModelSerializer(file_type=file_type)
            else:
                raise ValueError("{} not supported".format(file_path.suffix))

    @time_and_log(True)
    def read(self, file_type: str, from_s3=False):
        """Load file locally or from S3"""
        serializer = Serializer.get_correct_serializer(file_type=file_type)

        # download the file from AWS if the file does not exists
        if from_s3 and not config.aws_s3_bucket_name():
            raise ValueError("No AWS S3 bucket name specified in config.")
        # load from S3
        elif from_s3:
            logger.warning(
                {
                    "process": "Serializer.read",
                    "message": f"Downloading latest {file_type} from S3.",
                    "aws_bucket": config.aws_s3_bucket_name(),
                }
            )
            s3 = S3Handler(file_type=file_type)
            s3.download()
        # from local folder
        else:
            return serializer.read()

    @time_and_log(True)
    def write(self, file_id: _FileId, object: Any, to_s3: bool = False):
        """Serialize object with option to push to S3."""
        file_id = _FileId(file_id)
        serializer = Serializer.get_correct_serializer(file_id=file_id)

        # save locally
        serializer.write(object)

        # download the file from AWS if the file does not exists
        if to_s3 and not config.aws_s3_bucket_name():
            raise ValueError("No AWS S3 bucket name specified in config.")
        # load from S3
        elif to_s3:
            s3 = S3Handler(file_id)
            s3.upload()
            s3.list_dir("models")
            logger.warning(
                {
                    "process": "Service.write",
                    "message": f"Pushed {file_id.to_path()} to S3.",
                    "aws_bucket": config.aws_s3_bucket_name(),
                }
            )
        else:
            pass
