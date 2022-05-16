"""Module for class-based feature generation."""
import gc

import numpy as np
import pandas as pd
from data_loader import DataLoader
from logger import time_and_log


class DataAggregator:
    def __init__(self, data_io: DataLoader) -> None:
        self.data_io = data_io

    @time_and_log(False)
    def generate(self) -> None:
        raise NotImplementedError


class TargetData(DataAggregator):
    REQUIRED_DATASETS = ["applications"]

    @time_and_log(False)
    def generate(self) -> pd.DataFrame:
        df = self.data_io["applications"].copy()
        self.dataset = df[["sk_id_curr", "target"]]

        return self.dataset


class ApplicationFeatures(DataAggregator):

    REQUIRED_DATASETS = ["applications"]

    @classmethod
    def handle_missing_values(
        cls, df: pd.DataFrame, max_pct_missing: int = 40
    ) -> pd.DataFrame:
        df_missing_pct = (
            (df.isnull().sum() / df.shape[0] * 100)
            .sort_values(ascending=False)
            .round(1)
        )
        keep_columns = df_missing_pct[
            df_missing_pct <= max_pct_missing
        ].index.tolist() + ["ext_source_1"]
        return df[keep_columns]

    @classmethod
    def handle_outliers(cls, df: pd.DataFrame) -> pd.DataFrame:
        # Replace the anomalous values with nan
        df["days_employed"].replace(365243, np.nan, inplace=True)

        return df

    @classmethod
    @time_and_log(False)
    def preprocess(cls, df: pd.DataFrame) -> pd.DataFrame:
        # Optional: Remove 4 applications with XNA CODE_GENDER (train set)
        df.drop("target", axis=1, inplace=True)
        df = df.select_dtypes("number")

        df = cls.handle_missing_values(df)
        df = cls.handle_outliers(df)

        return df

    @time_and_log(False)
    def generate(self) -> pd.DataFrame:
        df = self.data_io["applications"].copy()
        print("Samples: {}".format(len(df)))

        df = ApplicationFeatures.preprocess(df)

        gc.collect()

        self.dataset = df

        return df
