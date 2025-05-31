from typing import Optional

import numpy as np
import polars as pl

from .base import CLUSTER_COL_NAME, ClusteringMethod, ClusteringMethodName
from .utils.distances import DistanceMethodName, DistanceManager

class KMedoids(ClusteringMethod):
    name = ClusteringMethodName.K_MEDOID

    def __init__(
        self,
        k: int,
        distance_method_name: Optional[str] = None,
    ):
        self.k = k
        self._distance_method_name = distance_method_name or DistanceMethodName.EUCLIDEAN.value
        self.distance_method = DistanceManager[self._distance_method_name]()

    def clustering(self, dataframe: pl.DataFrame) -> tuple[pl.DataFrame, np.ndarray]:
        dataframe = dataframe.clone()
        data_np = dataframe.to_numpy()
        n = data_np.shape[0]

        medoid_indices = np.random.choice(n, self.k, replace=False)
        medoids = data_np[medoid_indices]

        while True:
            clusters = self._get_clusters(data_np, medoids)
            new_medoid_indices = self._update_medoids(data_np, clusters)

            if np.array_equal(medoid_indices, new_medoid_indices):
                break

            medoid_indices = new_medoid_indices
            medoids = data_np[medoid_indices]

        dataframe = dataframe.with_columns(
            pl.Series(name=CLUSTER_COL_NAME, values=clusters)
        )
        return dataframe, medoids

    def _get_clusters(self, data: np.ndarray, medoids: np.ndarray) -> np.ndarray:
        distances = np.array([
            [self.distance_method.distance(point, medoid) for medoid in medoids]
            for point in data
        ])
        return np.argmin(distances, axis=1)

    def _update_medoids(self, data: np.ndarray, clusters: np.ndarray) -> np.ndarray:
        new_medoid_indices = []

        for i in range(self.k):
            cluster_points = data[clusters == i]

            if len(cluster_points) == 0:
                new_medoid_indices.append(np.random.randint(0, len(data)))
                continue

            total_distances = np.array([
                sum(self.distance_method.distance(p1, p2) for p2 in cluster_points)
                for p1 in cluster_points
            ])
            best_idx = np.argmin(total_distances)
            mask = np.isclose(data, cluster_points[best_idx], atol=1e-8).all(axis=1)
            real_index = np.where(mask)[0][0]
            new_medoid_indices.append(real_index)

        return np.array(new_medoid_indices)
