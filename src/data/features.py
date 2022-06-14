"""Module for class-based feature generation."""
import gc
from typing import Optional

import numpy as np
import pandas as pd
from logger import time_and_log
from data.load import FileDataLoader


class TargetData:
    REQUIRED_DATASETS = ["applications"]

    def __init__(self, data_io: FileDataLoader):
        self.data_io = data_io

    @time_and_log(False)
    def generate(self) -> pd.DataFrame:
        df = self.data_io["applications"].copy()
        self.dataset = df[["sk_id_curr", "target"]]

        return self.dataset


class DataAggregator:
    """Base data aggregator."""

    def __init__(self, data_io: Optional[FileDataLoader] = None, flow: str = "train"):
        if flow == "train":
            assert data_io is not None
            self.data_io = data_io
        self.flow_ = flow


class ApplicationFeatures(DataAggregator):

    REQUIRED_DATASETS = ["applications"]

    def handle_missing_values(
        self, df: pd.DataFrame, max_pct_missing: int = 40
    ) -> pd.DataFrame:
        if self.flow_ == "train":
            df_missing_pct = (
                (df.isnull().sum() / df.shape[0] * 100)
                .sort_values(ascending=False)
                .round(1)
            )
            keep_columns = df_missing_pct[
                df_missing_pct <= max_pct_missing
            ].index.tolist() + ["ext_source_1"]
            return df[keep_columns]
        else:
            return df

    def handle_outliers(self, df: pd.DataFrame) -> pd.DataFrame:
        # Replace the anomalous values with nan
        df["days_employed"].replace(365243, np.nan, inplace=True)

        return df

    @time_and_log(False)
    def preprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        if self.flow_ == "train":
            df.drop("target", axis=1, inplace=True)
            df = df.select_dtypes(include=np.number)

        df = self.handle_missing_values(df)
        df = self.handle_outliers(df)

        return df

    @time_and_log(False)
    def generate(self, df: Optional[pd.DataFrame] = None) -> pd.DataFrame:

        if self.flow_ == "train":
            df = self.data_io["applications"].copy()
        else:
            assert df is not None

        df = self.preprocess(df)

        gc.collect()

        self.dataset = df

        return df
