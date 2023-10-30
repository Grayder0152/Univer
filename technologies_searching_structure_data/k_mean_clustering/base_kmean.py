from abc import ABC, abstractmethod

from pyspark.sql import DataFrame


class BaseKMean(ABC):
    cluster_col_name: str = 'cluster'

    def __init__(
            self, data: DataFrame, k: int,
            pk_col_name: str, columns_params: list[str],
            **kwargs
    ):
        self.data = data
        self.k: int = k
        self.pk_col_name: str = pk_col_name
        self.columns_params: list[str] = columns_params

        self.last_centroids = None
        self.last_clustered_data = None

    @property
    def columns_params(self):
        return self.__columns_params

    @columns_params.setter
    def columns_params(self, value: list[str]):
        if not isinstance(value, list) or len(value) < 2:
            raise ValueError('Column parameters must be a list with min 2 values.')
        self.__columns_params = value

    @abstractmethod
    def clustering(self) -> None:
        pass
