from pathlib import Path
import os
from typing import List
import sqlalchemy

TITLE = "DOP Ranking"
DESCRIPTION = "Rank drop of points based on demand and supply."

"""Infra Related Environment Variables."""
DEBUG = os.getenv("DEBUG", False)
TIMEZONE = os.getenv("TIMEZONE", default="UTC")
STAGE = os.getenv("STAGE", "")
GIT_COMMIT_HASH = os.getenv("GIT_COMMIT_HASH", "")

WORK_DIR = os.getenv("WORKDIR", "")
LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", "INFO")

# AWS
AWS_S3_BUCKET = os.getenv("AWS_S3_BUCKET_NAME")
AWS_REDSHIFT_USERNAME = os.getenv("AWS_REDSHIFT_USERNAME")
AWS_REDSHIFT_PASSWORD = os.getenv("AWS_REDSHIFT_PASSWORD")

""" getters """


def queries_folder() -> Path:
    return work_dir() / "src/data/queries"


def aws_s3_bucket_name() -> str:
    return "home-credit-risk-dev"


def dwh_connection() -> sqlalchemy.engine.base.Engine:
    """Connect to Redshift database."""

    # build the sqlalchemy URL
    url = sqlalchemy.engine.url.URL.create(
        drivername="redshift+redshift_connector",
        host="ml-cluster.cao3kphpeedo.us-east-1.redshift.amazonaws.com",
        port=5439,
        database="dev",
        username=AWS_REDSHIFT_USERNAME,
        password=AWS_REDSHIFT_PASSWORD,
    )

    engine = sqlalchemy.create_engine(url)
    return engine


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
