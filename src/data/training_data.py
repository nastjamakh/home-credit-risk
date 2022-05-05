"""Module for class-based feature generation."""
import re
from typing import List
from functools import reduce
import pandas as pd

from data_io import DataLoader
from data.agreggators import TargetData, DataAggregator

from logger import time_and_log


class TrainingData:
    def __init__(
        self,
        data_io: DataLoader,
        target: TargetData,
        features: List[DataAggregator],
        merge_on="sk_id_curr",
    ):
        """Initialize."""
        self.target = target(data_io=data_io)

        self.features = []
        for feature in features:
            self.features.append(feature(data_io=data_io))

        self.merge_on = merge_on

    @time_and_log(False)
    def post_process(self):
        """Remove special characters form column names."""
        self.training_data = self.training_data.rename(
            columns=lambda x: re.sub("[^A-Za-z0-9_]+", "", x)
        )

    @time_and_log(False)
    def generate_training_dataset(self):
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
