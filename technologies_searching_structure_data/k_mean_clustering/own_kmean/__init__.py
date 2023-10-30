from typing import Type

import pyspark.sql.functions as f

from pyspark.pandas import DataFrame
from pyspark.sql import Window
from pyspark.sql.types import FloatType
from scipy.spatial import distance

from base_kmean import BaseKMean
from own_kmean.centroid_methods import CentroidMethod, CentroidMethodName, KMeanPp


class KMean(BaseKMean):
    centroid_methods: dict[CentroidMethodName, Type[CentroidMethod]] = {
        KMeanPp.name: KMeanPp
    }

    def __init__(
            self, data: DataFrame, k: int,
            pk_col_name: str, columns_params: list[str],
            centroid_method: str = 'k-mean++'
    ):
        super().__init__(data, k, pk_col_name, columns_params)
        self.data: DataFrame = (
            self.data
            .select(pk_col_name, *columns_params)
            .withColumn('coords', f.array(*columns_params))
        )
        self.centroid_method: CentroidMethod = self.centroid_methods[CentroidMethodName(centroid_method)](
            self.data, k, pk_col_name, columns_params
        )

    def clustering(self):
        distance_udf = f.udf(lambda point_1, point_2: float(distance.euclidean(point_1, point_2)), FloatType())
        window = Window.partitionBy(self.pk_col_name).orderBy('distance')

        self.last_centroids = (
            self.centroid_method.get_centroids()
            .select(f.col(self.pk_col_name).alias(self.cluster_col_name), *self.columns_params)
        )
        self.last_clustered_data = (
            self.data
            .crossJoin(
                self.last_centroids
                .withColumn('centroid_coords', f.array(*self.columns_params))
                .drop(*self.columns_params)
            ).withColumn('distance', distance_udf('coords', 'centroid_coords'))
            .withColumn('row', f.row_number().over(window))
            .where(f.col('row') == 1)
            .select(self.pk_col_name, *self.columns_params, self.cluster_col_name)
        )
