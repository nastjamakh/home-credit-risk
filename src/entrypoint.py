"""CLI interface."""
import fire

from train import TrainingPipeline
from data.load import FileDataLoader
from modelling.estimator import HeuristicEstimator


class Entrypoint:
    """CLI entrypoint."""

    def __init__(self) -> None:
        self.train = TrainingPipeline()
        self.data = FileDataLoader()
        self.model = HeuristicEstimator()


def cli() -> None:
    """Function to start cli."""
    fire.Fire(Entrypoint)


if __name__ == "__main__":
    cli()
