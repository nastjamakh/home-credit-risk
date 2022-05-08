import os

import boto3
import botocore
import config
import fire
from logger import logger, time_and_log

from serialization.utils import _FileId


class S3Handler:
    """Download / Upload files on S3"""

    def __init__(self) -> None:
        """Initialize."""
        s3_config = botocore.client.Config(
            connect_timeout=5, retries={"max_attempts": 5}
        )
        self.s3 = boto3.resource("s3", config=s3_config)
        self.bucket_name = config.aws_s3_bucket_name()
        self.bucket = self.s3.Bucket(self.bucket_name)

    def list_dir(self, dirname: str) -> list:

        response = boto3.client("s3").list_objects_v2(
            Bucket=self.bucket_name, Prefix=dirname
        )["Contents"]
        return response

    def get_latest_file(self, dirname: str) -> str:
        response = self.list_dir(dirname)
        latest = max(response, key=lambda x: x["LastModified"])["Key"]
        return latest

    @time_and_log(False)
    def download(self, file_type: str) -> None:
        """Download from S3."""
        dirname = f"{file_type}s"
        filepath_s3 = self.get_latest_file(dirname)
        filepath_local = str(filepath_s3)
        logger.info(
            {
                "message": "Downloading from S3.",
                "filepath_local": filepath_local,
                "filepath_s3": filepath_s3,
                "bucket": self.bucket_name,
            }
        )
        if not os.path.exists(dirname):
            os.mkdir(dirname)
        self.bucket.download_file(filepath_s3, filepath_local)

    @time_and_log(False)
    def upload(self, file_id: _FileId) -> None:
        """Push to S3."""
        filepath_local = str(file_id.to_path())
        logger.info(
            {
                "message": "Uploading to S3.",
                "filepath_local": filepath_local,
                "filepath_s3": file_id.to_s3_key(),
                "bucket": self.bucket_name,
            }
        )
        self.s3.meta.client.upload_file(
            filepath_local, self.bucket_name, file_id.to_s3_key()
        )


def cli() -> None:
    """CLI interface for training and evaluation."""
    fire.Fire(S3Handler)


if __name__ == "__main__":
    cli()
