from lightgbm import LGBMClassifier


class Estimator:
    def __init__(self):
        self.model = LGBMClassifier()
