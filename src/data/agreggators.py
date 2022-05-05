"""Module for class-based feature generation."""
import pandas as pd
import numpy as np
import gc

from data_io import DataLoader
from data.transformers import OneHotEncoderWithMemory

from logger import time_and_log


class DataAggregator:
    def __init__(self, data_io: DataLoader):
        self.data_io = data_io

    @time_and_log(False)
    def generate(self):
        raise NotImplementedError


class TargetData(DataAggregator):
    REQUIRED_DATASETS = ["applications"]

    @time_and_log(False)
    def generate(self) -> pd.DataFrame:
        df = self.data_io["applications"].copy()
        self.dataset = df[["sk_id_curr", "target"]]

        return self.dataset


class ApplicationFeatures(DataAggregator):

    BIN_FEATURES = ["code_gender", "flag_own_car", "flag_own_realty"]
    REQUIRED_DATASETS = ["applications"]

    @classmethod
    @time_and_log(False)
    def preprocess(cls, df: pd.DataFrame) -> pd.DataFrame:
        # Optional: Remove 4 applications with XNA CODE_GENDER (train set)
        df.drop("target", axis=1, inplace=True)
        df = df[df["code_gender"] != "XNA"]

        # Categorical features with Binary encode (0 or 1; two categories)
        for bin_feature in cls.BIN_FEATURES:
            df.loc[:, bin_feature], uniques = pd.factorize(df.loc[:, bin_feature])
        # Categorical features with One-Hot encode
        encoder = OneHotEncoderWithMemory(nan_category=False)
        df = encoder.fit_transform(df)

        # NaN values for days_employed: 365.243 -> nan
        df["days_employed"].replace(365243, np.nan, inplace=True)

        return df

    @staticmethod
    @time_and_log(False)
    def add_new_features(df):
        df["days_employed_perc"] = df["days_employed"] / df["days_birth"]
        df["income_credit_perc"] = df["amt_income_total"] / df["amt_credit"]
        df["income_per_person"] = df["amt_income_total"] / df["cnt_fam_members"]
        df["annuity_income_perc"] = df["amt_annuity"] / df["amt_income_total"]
        df["payment_rate"] = df["amt_annuity"] / df["amt_credit"]
        return df

    @time_and_log(False)
    def generate(self):
        df = self.data_io["applications"].copy()
        print("Samples: {}".format(len(df)))

        df = ApplicationFeatures.preprocess(df)
        df = ApplicationFeatures.add_new_features(df)

        gc.collect()

        self.dataset = df

        return df
