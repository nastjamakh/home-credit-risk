"""Module for class-based feature generation."""
import re

from data_io import DataLoader
from data.agreggators import ApplicationFeatures, TargetData


class TrainingData:
    def __init__(
        self,
        data_io: DataLoader,
        target: TargetData,
        app_data: ApplicationFeatures,
        merge_on="sk_id_curr",
    ):
        """Initialize."""
        self.target = target(data_io=data_io)
        self.app_data = app_data(data_io=data_io)
        self.merge_on = merge_on

    def generate_training_dataset(self):
        print("Generating training dataset.")
        self.target.generate_target()
        self.app_data.generate_features()

        df = self.target.dataset.merge(
            self.app_data.dataset, how="left", on=self.merge_on
        )
        df = df.rename(columns=lambda x: re.sub("[^A-Za-z0-9_]+", "", x))
        self.training_data = df
        print("Done.")

        return df
