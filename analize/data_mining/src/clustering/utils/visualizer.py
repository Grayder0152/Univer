from abc import ABC, abstractmethod
from typing import Optional

import matplotlib.pyplot as plt
import numpy as np
import polars as pl

from settings import CLUSTER_COL_NAME


class BaseVisualizer(ABC):
    figure = None
    axis = None

    def __init__(self, **kwargs) -> None:
        self.figure, self.axis = plt.subplots(1, 1, **kwargs)

    @abstractmethod
    def plot(self, dataframe: pl.DataFrame, feature_names: Optional[list] = None) -> None:
        pass

    @staticmethod
    def show():
        plt.show()


class VisualizerND(BaseVisualizer):
    figure = None
    axis = None

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.axis.set_title(f'{self.feature_count}D Visualization of Clusters')

    @property
    @abstractmethod
    def feature_count(self) -> int:
        pass

    def add_centroids(self, centroids: np.array) -> None:
        self.axis.scatter(*[centroids[:, i] for i in range(self.feature_count)], s=70, label='Centroids')
        self.axis.legend()


class Visualizer2DNoClustered(VisualizerND):
    feature_count = 2

    def plot(self, dataframe: pl.DataFrame, feature_names: Optional[list[str]] = None) -> None:
        if feature_names:
            if len(feature_names) != self.feature_count:
                raise ValueError('Incorrect amount of feature names provided.')
            feature_1, feature_2 = feature_names
        else:
            feature_1, feature_2 = dataframe.columns[:self.feature_count]
        self.axis.set_xlabel(feature_1)
        self.axis.set_ylabel(feature_2)
        self.axis.scatter(dataframe[feature_1], dataframe[feature_2])


class Visualizer2D(VisualizerND):
    feature_count = 2

    def plot(
        self,
        dataframe: pl.DataFrame,
        feature_names: Optional[list[str]] = None,
        centroids: Optional[np.ndarray] = None,
    ) -> None:
        if feature_names:
            if len(feature_names) != self.feature_count:
                raise ValueError('Incorrect amount of feature names provided.')
            feature_1, feature_2 = feature_names
        else:
            feature_1, feature_2 = dataframe.drop(CLUSTER_COL_NAME).columns[:self.feature_count]

        clusters = sorted(dataframe.select(CLUSTER_COL_NAME).unique().to_series().to_list())

        self.axis.set_xlabel(feature_1)
        self.axis.set_ylabel(feature_2)

        for cluster in clusters:
            cluster_data = dataframe.filter(pl.col(CLUSTER_COL_NAME) == cluster)
            self.axis.scatter(
                cluster_data[feature_1],
                cluster_data[feature_2],
                label=f'Cluster {cluster}',
                alpha=0.6
            )

        # Додаємо центроїди, якщо передані
        if centroids is not None:
            for i, centroid in enumerate(centroids):
                self.axis.scatter(
                    centroid[0], centroid[1],
                    marker='x', s=50, c='black', label=f'Centroid {i}'
                )

        self.axis.legend()
