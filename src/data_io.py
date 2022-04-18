"""Module to load data."""
import os
import gc
import pandas as pd
from enum import Enum
from tqdm import tqdm
from pathlib import Path

from config import data_dir
from logger import time_and_log


def preprocess_description_data() -> None:
    """Preprocess description data."""
    """Clean up descriptions dataset."""
    path = data_dir() / "HomeCredit_columns_description.csv"

    with open(path, "r", newline="", encoding="ISO-8859-1") as csvfile:
        df = pd.read_csv(csvfile, index_col=[0])

    df.columns = [col.lower() for col in df.columns]
    df.table = df.table.apply(
        lambda col: "applications"
        if col == "application_{train|test}.csv"
        else col.split(".csv")[0]
    )
    df["row"] = df["row"].str.lower()

    df.to_csv(
        data_dir() / "HomeCredit_columns_description_processed.csv",
        encoding="utf-8",
        index=False,
    )


class DatasetFilename(Enum):
    """Map dataset names to filepaths."""

    APPLICATIONS = "application_train.gzip"
    BUREAU_BALANCE = "bureau_balance.gzip"
    BUREAU = "bureau.gzip"
    CREDIT_CARD_BALANCE = "credit_card_balance.gzip"
    INSTALLMENTS_PAYMENTS = "installments_payments.gzip"
    PREVIOUS_APPLICATIONS = "previous_application.gzip"
    CASH_BALANCE = "POS_CASH_balance.gzip"

    @classmethod
    def from_name(cls, name):
        if hasattr(DatasetFilename, name.upper()):
            return getattr(DatasetFilename, name.upper()).value
        else:
            raise ValueError(f"No such dataset: {name}")


class DataLoader:
    """Class to load data from file."""

    DATASETS = [
        name.split(".")[0].lower() for name, _ in DatasetFilename.__members__.items()
    ]

    DESCRIPTIONS_FILENAME = "HomeCredit_columns_description_processed.csv"

    def __init__(self) -> None:
        """Initialize class instance."""

        # store loaded datasets
        self.datasets_ = dict()

    @staticmethod
    def preprocess_dataset(df) -> pd.DataFrame:
        df.columns = [col.lower() for col in df.columns]

        # lowercast all string columns
        for col, dt in zip(df.columns, df.dtypes):
            if dt == object:
                df[col] = df[col].str.lower()
                gc.collect()
        return df

    @time_and_log(True)
    def load_dataset(self, dataset_name: str) -> pd.DataFrame:
        assert dataset_name in self.DATASETS, f"Unknown dataset {dataset_name}."

        if dataset_name in self.datasets_:
            df = self.datasets_[dataset_name]
        else:
            df = pd.read_parquet(data_dir() / DatasetFilename.from_name(dataset_name))

            self.datasets_[dataset_name] = df

        df = self.preprocess_dataset(df)
        gc.collect()
        return df

    @time_and_log(False)
    def load_all(self) -> None:
        """List all datasets."""
        pbar = tqdm(self.DATASETS)
        for dataset in pbar:
            pbar.set_description(f"Loading dataset: {dataset}")
            self.load_dataset(dataset_name=dataset)

    @classmethod
    def list_available(cls) -> list:
        """List all availbale datasets."""
        return cls.DATASETS

    def list_loaded(self) -> list:
        """List all loaded datasets."""
        return list(self.datasets_.keys())

    @classmethod
    def get_dataset_filepath(cls, dataset_name: str) -> Path:
        """Return filepath of a dataset."""
        return data_dir() / DatasetFilename.from_name(dataset_name)

    def __getitem__(self, dataset_name: str) -> pd.DataFrame:
        """Use class as a dict with keys as dataset names."""
        assert dataset_name in self.datasets_, f"Dataset {dataset_name} is not loaded."
        return self.datasets_[dataset_name]

    @classmethod
    def describe_columns(cls, dataset_name: str) -> pd.DataFrame:
        """Describe dataset columns."""
        if not os.path.exists(data_dir() / cls.DESCRIPTIONS_FILENAME):
            preprocess_description_data()
        return pd.read_csv(
            data_dir() / cls.DESCRIPTIONS_FILENAME, encoding="utf-8"
        ).query("table == @dataset_name")[["row", "description"]]
