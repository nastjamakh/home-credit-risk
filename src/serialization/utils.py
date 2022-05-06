"""Final estimator."""
import os
import re
from datetime import datetime
from pathlib import Path

from config import model_dir

MODEL_FILENAME_PATTERN = "(?<=model_)(.*)(?=.joblib)"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"


def model_filename_from_datetime(dt: datetime) -> str:
    """Build model filename from datetime using correct format."""
    return f"model_{dt.strftime(DATETIME_FORMAT)}.joblib"


def str_to_datetime(datetime_string: str) -> datetime:
    """Convert string to datetime in required format."""
    return datetime.strptime(datetime_string, DATETIME_FORMAT)


def extract_model_timestamp(filename: str) -> str:
    """Extract timestamp form model filename."""
    return re.findall(MODEL_FILENAME_PATTERN, filename)[0]


def get_latest_model_file_id(s3=False) -> str:
    """Get filename of the latest model created."""
    files = os.listdir(model_dir())
    latest_model_dt = sorted(
        [str_to_datetime(extract_model_timestamp(f)) for f in files],
        reverse=True,
    )[0]
    return model_filename_from_datetime(latest_model_dt)


class _FileId:
    """
    file_id app/home-credit-risk/models/model_23324.joblib
    s3_key models/model_23324.joblib
    path app/home-credit-risk/models/model_23324.joblib
    """

    def __init__(self, fid: str) -> None:
        """Initialize."""
        self.fid = fid

    def to_s3_key(self):
        """Get associated filepath on S3 bucket.."""
        dirname = self.fid.parts[-2]
        filename = self.fid.name
        return str(os.path.join(dirname, filename))

    def to_path(self):
        """Get full file path."""
        return self._project_root() / self.fid

    def _project_root(self):
        """Get project root."""
        return Path(__file__).parent.parent

    def __str__(self):
        """String representation."""
        return str(self.fid)
