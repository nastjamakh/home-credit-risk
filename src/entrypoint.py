"""CLI interface."""
import fire

from train import TrainingPipeline
from data_loader import DataLoader
from modelling.estimator import HomeCreditEstimator


class Entrypoint:
    def __init__(self):
        self.train = TrainingPipeline()
        self.data = DataLoader()
        self.model = HomeCreditEstimator()


def cli():
    fire.Fire(Entrypoint)


if __name__ == "__main__":
    cli()
