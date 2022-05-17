"""Module for class-based feature generation."""
import re
from functools import reduce
from typing import List

import pandas as pd
from data_loader import DataLoader
from logger import time_and_log

from data.features import DataAggregator, TargetData


class TrainingData:
    def __init__(
        self,
        data_io: DataLoader,
        target: TargetData,
        features: List[DataAggregator],
        merge_on: str = "sk_id_curr",
    ):
        """Initialize."""
        self.target = target(data_io=data_io)

        self.features = []
        for feature in features:
            self.features.append(feature(data_io=data_io))

        self.merge_on = merge_on

    @time_and_log(False)
    def post_process(self) -> None:
        """Remove special characters form column names."""
        self.training_data: pd.DataFrame = self.training_data.rename(
            columns=lambda x: re.sub("[^A-Za-z0-9_]+", "", x)
        )

    @time_and_log(False)
    def generate_training_dataset(self) -> pd.DataFrame:
        print("Generating training dataset.")
        self.target.generate()
        for feature in self.features:
            feature.generate()

        features = reduce(
            lambda left, right: pd.merge(left, right, on="name"),
            [feature.dataset for feature in self.features],
        )
        self.training_data = self.target.dataset.merge(
            features, how="left", on=self.merge_on
        )

        self.post_process()

        return self.training_data
