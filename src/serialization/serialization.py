"""
    Responsabilities:
    - (De) Serialization
    - Download/Upload files to and from S3 if they dont exists locally
    - Model-Zoo
"""
import functools
import os
from pathlib import Path
from typing import Any

import boto3
import botocore
import config
import joblib
from logger import logger, time_and_log


@functools.lru_cache()
def get_model_from_zoo(latest=True):
    return Serializer().read(file_id=model_file_id(latest=latest))


def model_file_id(latest: bool = True):
    if latest:
        return "models/homecredit_.model"
    else:
        raise NotImplementedError


class _FileId:
    """
    file_id datasets/session_facts.csv
    s3_key versioning/datasets/session_facts.csv
    path ~/datasets/session_facts.csv
    """

    def __init__(self, fid: str) -> None:
        """Initialize."""
        self.fid = fid

    def to_s3_key(self):
        return str(Path("versioning") / self.fid)

    def to_path(self):
        return self._project_root() / self.fid

    def _project_root(self):
        return Path(__file__).parent.parent


class ModelSerializer:
    """object <-> file with joblib"""

    def __init__(self, file_id: _FileId) -> None:
        """Initialize."""
        self.file_id = file_id

    def read(self) -> None:
        """Load model from file."""
        return joblib.load(self.file_id.to_path())

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


class S3Handler:
    """Download / Upload files on S3"""

    def __init__(self, file_id: _FileId) -> None:
        """Initialize."""
        self.file_id = file_id
        s3_config = botocore.client.Config(
            connect_timeout=5, retries={"max_attempts": 5}
        )
        self.s3 = boto3.resource("s3", config=s3_config)
        self.bucket_name = config.aws_s3_bucket_name()

    def download(self) -> None:
        """Download from S3."""
        self.s3.Bucket(self.bucket_name).download_file(
            self.file_id.to_s3_key(), str(self.file_id.to_path())
        )

    def upload(self) -> None:
        """Push to S3."""
        self.s3.meta.client.upload_file(
            str(self.file_id.to_path()),
            self.bucket_name,
            self.file_id.to_s3_key(),
        )


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

    def __init__(self, file_id: str) -> None:
        self.file_id = _FileId(file_id)
        self.serializer_ = Serializer.get_correct_serializer(self.file_id)

    @staticmethod
    def get_correct_serializer(file_id: _FileId):
        file_path = file_id.to_path()

        if file_path.suffix == ".joblib":
            return ModelSerializer(file_id=file_id)
        else:
            raise ValueError("{} not supported".format(file_path.suffix))

    @time_and_log(True)
    def read(self, from_s3=False):
        """Load file locally or from S3"""

        # download the file from AWS if the file does not exists
        if from_s3 and not config.aws_s3_bucket_name():
            raise ValueError("No AWS S3 bucket name specified in config.")
        # load from S3
        elif from_s3:
            logger.warning(
                {
                    "process": "Serializer.read",
                    "message": f"Downloading {self.file_id} from S3.",
                    "aws_bucket": config.aws_s3_bucket_name(),
                }
            )
            S3Handler(self.file_id).download()
        # from local folder
        else:
            return self.serializer_.read()

    @time_and_log(True)
    def write(self, object: Any, to_s3: bool = False):
        """Serialize object with option to push to S3."""

        # save locally
        self.serializer_.write(object)

        # download the file from AWS if the file does not exists
        if to_s3 and not config.aws_s3_bucket_name():
            raise ValueError("No AWS S3 bucket name specified in config.")
        # load from S3
        elif to_s3:
            S3Handler(self.file_id).upload()
            logger.warning(
                {
                    "process": "Service.write",
                    "message": f"Pushed {self.file_id.to_path()} to S3.",
                    "aws_bucket": config.aws_s3_bucket_name(),
                }
            )
        else:
            pass
