"""Module for class-based feature generation."""
from typing import List
import pandas as pd

from data.agreggators import DataAggregator


class TargetData(DataAggregator):
    @classmethod
    def name(cls) -> str:
        """Name."""
        return "target"

    @classmethod
    def required_datasets(cls) -> List[str]:
        ["applications"]

    def feature_names(cls) -> List[str]:
        return ["target"]

    def generate_target(self):
        """Generate all feautres in this set."""
        return self.datasets_["applications"][["app_id", "target"]]


class TrainingDataset(pd.DataFrame):

    MERGE_ON = ["app_id"]

    def __init__(
        self, target_data: TargetData, aggregated_data_list: List[DataAggregator]
    ):
        self.check_target(target_data.df)

        for agg in aggregated_data_list:
            self.check_aggregator(agg.df)

        self.df = self.merge_(target_data, *aggregated_data_list)

    def check_target(self, target_data):
        pass

    def check_aggregator(self, agg):
        pass

    def merge_(self, df, *args):
        new_data = [a.df for a in args]

        df_new = df.merge(new_data, on=self.MERGE_ON, how="left")
        return df_new
