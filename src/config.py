from pathlib import Path
import os
from typing import List

TITLE = "DOP Ranking"
DESCRIPTION = "Rank drop of points based on demand and supply."

"""Infra Related Environment Variables."""
DEBUG = os.getenv("DEBUG", False)
TIMEZONE = os.getenv("TIMEZONE", default="UTC")
STAGE = os.getenv("STAGE", "")
GIT_COMMIT_HASH = os.getenv("GIT_COMMIT_HASH", "")

WORK_DIR = os.getenv("WORKDIR", "")
LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", "INFO")
AWS_S3_BUCKET = os.getenv("AWS_S3_BUCKET_NAME")

""" getters """


def queries_folder() -> Path:
    return work_dir() / "src/data/queries"


def aws_s3_bucket_name() -> str:
    return "home-credit-risk"


"""" getters """


def api_keys() -> List[str]:
    """Returns list of valid API keys."""
    return [v for k, v in os.environ.items() if k.startswith("API_KEY")]


def work_dir() -> Path:
    """Get working dir."""
    if WORK_DIR == "":
        return Path(__file__).parent.parent
    else:
        return Path(WORK_DIR)


def data_dir() -> Path:
    """Get data dir."""
    return work_dir() / "datasets"


def model_dir() -> Path:
    """Get model dir."""
    return work_dir() / "models"
