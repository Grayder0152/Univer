from abc import ABC, abstractmethod
from enum import StrEnum

import polars as pl

CLUSTER_COL_NAME = 'cluster'


class ClusteringMethodName(StrEnum):
    K_MEANS = "K-Means"
    K_MEDOID = "K-Medoids"

class ClusteringMethod(ABC):
    @property
    @abstractmethod
    def name(self) -> ClusteringMethodName:
        pass

    @staticmethod
    @abstractmethod
    def clustering(self, dataframe: pl.DataFrame) -> pl.DataFrame:
        pass

    def __repr__(self) -> str:
        return f'{self.name.value.title()} distance method'
