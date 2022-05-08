"""CLI interface."""
import fire

from train import TrainingPipeline
from data_loader import DataLoader
from modelling.estimator import HomeCreditEstimator


class Entrypoint:
    """CLI entrypoint."""

    def __init__(self) -> None:
        self.train = TrainingPipeline()
        self.data = DataLoader()
        self.model = HomeCreditEstimator()


def cli() -> None:
    """Function to start cli."""
    fire.Fire(Entrypoint)


if __name__ == "__main__":
    cli()
