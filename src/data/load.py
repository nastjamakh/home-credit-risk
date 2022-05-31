"""Module to load data."""
from abc import abstractmethod
import gc
import os
from enum import Enum
from pathlib import Path
from typing import Dict, Optional

import fire
import pandas as pd
from tqdm import tqdm

from config import data_dir, dwh_connection
from logger import time_and_log


def csv_to_parquet(delete_csv: bool = False) -> None:
    """Convert fiel from csv to parquet."""
    pass


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
    CASH_BALANCE = "pos_cash_balance.gzip"

    @classmethod
    def from_name(cls, name: str) -> str:
        if hasattr(DatasetFilename, name.upper()):
            return getattr(DatasetFilename, name.upper()).value
        else:
            raise ValueError(f"No such dataset: {name}")


class DatasetName(Enum):
    """Map dataset names to table names in database."""

    APPLICATIONS = "applications"
    BUREAU_BALANCE = "bureau_balance"
    BUREAU = "bureau"
    CREDIT_CARD_BALANCE = "credit_card_balance"
    INSTALLMENTS_PAYMENTS = "installments_payments"
    PREVIOUS_APPLICATIONS = "previous_applications"
    CASH_BALANCE = "pos_cash_balance"

    @classmethod
    def from_name(cls, name: str, file: bool = False) -> str:
        if hasattr(DatasetName, name.upper()):
            dataset_name = getattr(DatasetName, name.upper()).value
            if file:
                dataset_name += ".gzip"
            return dataset_name
        else:
            raise ValueError(f"No such dataset: {name}")


class DataLoader:
    DATASETS = [
        name.split(".")[0].lower() for name, _ in DatasetFilename.__members__.items()
    ]

    def __init__(self) -> None:
        """Initialize class instance."""

        # store loaded datasets
        self.datasets_: Dict[str, pd.DataFrame] = dict()

    @staticmethod
    def lowercase_columns(df: pd.DataFrame) -> pd.DataFrame:
        df.columns = [col.lower() for col in df.columns]

        # lowercast all string columns
        for col, dt in zip(df.columns, df.dtypes):
            if dt == object:
                df[col] = df[col].str.lower()
                gc.collect()
        return df

    @abstractmethod
    def load_dataset(self, dataset_name: str) -> pd.DataFrame:
        """Load a dataset by name."""
        pass

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

    def __getitem__(self, dataset_name: str) -> pd.DataFrame:
        """Use class as a dict with keys as dataset names."""
        assert dataset_name in self.datasets_, f"Dataset {dataset_name} is not loaded."
        return self.datasets_[dataset_name]


class FileDataLoader(DataLoader):
    """Class to load data from file."""

    DESCRIPTIONS_FILENAME = "HomeCredit_columns_description_processed.csv"

    @time_and_log(True)
    def load_dataset(self, dataset_name: str) -> pd.DataFrame:
        assert dataset_name in self.DATASETS, f"Unknown dataset {dataset_name}."

        if dataset_name in self.datasets_:
            df = self.datasets_[dataset_name]
        else:
            df = pd.read_parquet(data_dir() / DatasetFilename.from_name(dataset_name))

            self.datasets_[dataset_name] = df

        df = self.lowercase_columns(df)
        gc.collect()
        return df

    @classmethod
    def get_dataset_filepath(cls, dataset_name: str) -> Path:
        """Return filepath of a dataset."""
        return data_dir() / DatasetFilename.from_name(dataset_name)

    @classmethod
    def describe_columns(cls) -> pd.DataFrame:
        """Describe dataset columns."""
        if not os.path.exists(data_dir() / cls.DESCRIPTIONS_FILENAME):
            preprocess_description_data()
        return pd.read_csv(
            data_dir() / cls.DESCRIPTIONS_FILENAME, encoding="utf-8"
        ).query("table == @dataset_name")[["row", "description"]]


class SQLDataLoader(DataLoader):
    """Class to load raw data from Redshift database."""

    engine = dwh_connection()

    @time_and_log(True)
    def load_dataset(
        self, dataset_name: str, limit: Optional[int] = None, reload: bool = False
    ) -> pd.DataFrame:
        if (dataset_name not in self.datasets_) or reload:
            with self.engine.connect() as conn:
                table_name = DatasetName.from_name(dataset_name)
                limit_str = f" limit {limit}" if limit else ""
                df = pd.read_sql(
                    f"SELECT * FROM public.{table_name}{limit_str}", con=conn
                )
                self.datasets_[dataset_name] = df
        else:
            df = self.datasets_[dataset_name]
        return df


def cli() -> None:
    """CLI interface for Data Loader."""
    fire.Fire(FileDataLoader)


if __name__ == "__main__":
    cli()
