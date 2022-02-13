"""Module for class-based feature generation."""
from abc import ABC, abstractmethod
from typing import List


class DataAggregator(ABC):
    @abstractmethod
    @classmethod
    def name(cls) -> str:
        """Name."""
        pass

    @abstractmethod
    @classmethod
    def required_datasets(cls) -> List[str]:
        pass

    @abstractmethod
    @classmethod
    def feature_names(cls) -> List[str]:
        pass

    def __init__(self, dataset_dict: dict):
        passed_datasets = set(dataset_dict.keys())
        required_datasets = set(self.required_datasets())

        assert required_datasets.issubset(
            passed_datasets
        ), f"Missing required datasets: {required_datasets - passed_datasets}"
        assert passed_datasets.issubset(
            required_datasets
        ), f"Too many datasets passed: {passed_datasets - required_datasets}"

        self.datasets_ = dataset_dict
        self.df = None

    def generate_features(self):
        """Generate all feautres in this set."""
        for feature_name in self.feature_names():
            getattr(self, feature_name)()


class ApartementData(DataAggregator):
    @classmethod
    def name(cls) -> str:
        """Name."""
        return "apartment"

    @abstractmethod
    @classmethod
    def required_datasets(cls) -> List[str]:
        return ["applications"]

    @abstractmethod
    @classmethod
    def feature_names(cls) -> List[str]:
        ["apt_size", "num_floors"]

    def __init__(self, dataset_dict: dict):
        super().__init__(dataset_dict=dataset_dict)

    def feature_apt_size(self):
        pass

    def feature_num_floors(self):
        pass
