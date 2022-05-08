""" Transformers. """
from sklearn.base import TransformerMixin, BaseEstimator
import pandas as pd


class OneHotEncoderWithMemory(TransformerMixin, BaseEstimator):
    """OneHot encoder that stores list of new dummy columns"""

    def __init__(self, nan_category: bool = True) -> None:
        self.nan_category = nan_category

    def fit(self, X: pd.DataFrame) -> "OneHotEncoderWithMemory":
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        original_columns = list(X.columns)
        categorical_columns = [col for col in X.columns if X[col].dtype == "object"]
        df = pd.get_dummies(X, columns=categorical_columns, dummy_na=self.nan_category)
        self.encoded_columns_ = [c for c in df.columns if c not in original_columns]

        return df
