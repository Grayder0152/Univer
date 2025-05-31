from typing import Optional

import numpy as np
import polars as pl

from .base import CLUSTER_COL_NAME, ClusteringMethod, ClusteringMethodName
from .utils.centroid_methods import CentroidMethodName, CentroidManager
from .utils.distances import DistanceMethodName, DistanceManager


class KMeans(ClusteringMethod):
    name = ClusteringMethodName.K_MEANS

    def __init__(
            self, k: int,
            distance_method_name: Optional[str] = None,
            centroid_method_name: Optional[str] = None
    ):
        self._distance_method_name = distance_method_name or DistanceMethodName.EUCLIDEAN.value
        self._centroid_method_name = centroid_method_name or CentroidMethodName.K_MEAN_PP.value

        self.k = k
        self.distance_method = DistanceManager[self._distance_method_name]()

    def clustering(self, dataframe: pl.DataFrame) -> tuple[pl.DataFrame, np.ndarray | pl.DataFrame]:
        centroid_method = CentroidManager[self._centroid_method_name](
            k=self.k, distance_method_name=self._distance_method_name
        )
        dataframe = dataframe.clone()
        centroids = centroid_method.get_centroids(dataframe)

        while True:
            clusters = self._get_clusters(dataframe, centroids)
            new_centroids = self._update_centroids(dataframe, clusters)
            if np.allclose(centroids, new_centroids, atol=1e-6):
                break
            centroids = new_centroids

        dataframe = dataframe.with_columns(
            pl.Series(name=CLUSTER_COL_NAME, values=clusters)
        )

        return dataframe, centroids

    def _get_clusters(self, dataframe: pl.DataFrame, centroids: np.array) -> np.array:
        data_np = dataframe.to_numpy()
        distances = np.array([
            [self.distance_method.distance(x, centroid) for centroid in centroids]
            for x in data_np
        ])
        return np.argmin(distances, axis=1)

    def _update_centroids(self, dataframe: pl.DataFrame, clusters: np.ndarray) -> np.ndarray:
        new_centroids = []
        df_np = dataframe.to_numpy()

        for i in range(self.k):
            points = df_np[clusters == i]
            if len(points) > 0:
                new_centroid = np.mean(points, axis=0)
            else:
                new_centroid = np.random.rand(df_np.shape[1])
            new_centroids.append(new_centroid)

        return np.array(new_centroids)
