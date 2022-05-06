import boto3
import botocore
import config
from logger import logger, time_and_log
import fire

from serialization.utils import _FileId


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
        self.bucket = self.s3.Bucket(self.bucket_name)

    def list_dir(self, dirname: str):

        response = boto3.client("s3").list_objects_v2(
            Bucket=self.bucket_name, Prefix=dirname
        )["Contents"]
        return response

    def get_latest_file(self, dirname: str) -> str:
        response = self.list_dir(dirname)
        latest = max(response, key=lambda x: x["LastModified"])
        return latest.key

    @time_and_log(False)
    def download(self, latest=True, filename=None) -> None:
        """Download from S3."""
        filepath_local = str(self.file_id.to_path())
        if latest:
            dirname = self.file_id.parts[-2]
            filename_s3 = self.get_latest_file(dirname)
            filepath_s3 = str(dirname / filename_s3)
            filepath_local = self.file_id.parent / filename_s3
        logger.debug(
            {
                "message": "Downloading from S3.",
                "filepath_local": filepath_local,
                "filepath_s3": filepath_s3,
                "bucket": self.bucket_name,
            }
        )
        self.bucket.download_file(self.file_id.to_s3_key(), filepath_local)

    @time_and_log(False)
    def upload(self) -> None:
        """Push to S3."""
        filepath_local = str(self.file_id.to_path())
        logger.debug(
            {
                "message": "Uploading to S3.",
                "filepath_local": filepath_local,
                "filepath_s3": self.file_id.to_s3_key(),
                "bucket": self.bucket_name,
            }
        )
        self.s3.meta.client.upload_file(
            filepath_local, self.bucket_name, self.file_id.to_s3_key()
        )


def cli():
    """CLI interface for training and evaluation."""
    fire.Fire(S3Handler)


if __name__ == "__main__":
    cli()
