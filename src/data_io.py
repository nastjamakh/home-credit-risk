"""Module to load data."""
import pandas as pd
from enum import Enum
from tqdm import tqdm

from config import data_dir


class DatasetFilename(Enum):
    APPLICATIONS = "application_train.feather"
    BUREAU_BALANCE = "bureau_balance.feather"
    BUREAU = "bureau.feather"
    CREDIT_CARD_BALANCE = "credit_card_balance.feather"
    INSTALLMENTS_PAYMENTS = "installments_payments.feather"
    PREVIOUS_APPLICATIONS = "previous_application.feather"
    CASH_BALANCE = "POS_CASH_balance.feather"

    @classmethod
    def from_name(cls, name):
        if hasattr(DatasetFilename, name.upper()):
            return getattr(DatasetFilename, name.upper()).value
        else:
            raise ValueError(f"No such dataset: {name}")


class Datasets:

    DATASETS = [
        name.split(".")[0].lower() for name, _ in DatasetFilename.__members__.items()
    ]

    DESCRIPTIONS_FILENAME = "HomeCredit_columns_description.csv"

    def __init__(self):

        # store loaded datasets
        self.datasets_ = dict()

    @staticmethod
    def format_dataset(df):
        df.columns = [col.lower() for col in df.columns]
        return df

    def load_dataset(self, dataset_name: str) -> pd.DataFrame:
        assert dataset_name in self.DATASETS, f"Unknown dataset {dataset_name}."

        if dataset_name in self.datasets_:
            df = self.datasets_[dataset_name]
        else:
            df = pd.read_feather(data_dir() / DatasetFilename.from_name(dataset_name))
            self.datasets_[dataset_name] = df

        df = self.format_dataset(df)
        return df

    def load_all(self):
        pbar = tqdm(self.DATASETS)
        for dataset in pbar:
            pbar.set_description(f"Loading dataset: {dataset}")
            self.load_dataset(dataset_name=dataset)

    @classmethod
    def list_available(cls) -> list:
        return cls.DATASETS

    def list_loaded(self) -> list:
        return list(self.datasets_.keys())

    def __getitem__(self, dataset_name: str) -> pd.DataFrame:
        assert dataset_name in self.datasets_, f"Dataset {dataset_name} is not loaded."
        return self.datasets_[dataset_name]

    @classmethod
    def describe_columns(cls, dataset_name: str) -> pd.DataFrame:
        return pd.read_csv(
            data_dir() / cls.DESCRIPTIONS_FILENAME, encoding="utf-8"
        ).query("table == @dataset_name")[["row", "description"]]
