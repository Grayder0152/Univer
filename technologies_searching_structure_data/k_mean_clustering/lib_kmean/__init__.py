from pyspark.ml.clustering import KMeans
from pyspark.ml.feature import StandardScaler, VectorAssembler
from pyspark.sql import DataFrame

from base_kmean import BaseKMean


class KMean(BaseKMean):
    def __init__(
            self, data: DataFrame, k: int,
            pk_col_name: str, columns_params: list[str]
    ):
        super().__init__(data, k, pk_col_name, columns_params)

    def clustering(self) -> None:
        kmeans = KMeans(featuresCol='scaled_data', predictionCol=self.cluster_col_name, k=self.k)

        data = VectorAssembler(inputCols=self.columns_params, outputCol='vector_data').transform(self.data)

        scaler = StandardScaler(
            inputCol="vector_data",
            outputCol="scaled_data",
            withStd=True,
            withMean=False
        )
        scaler_model = scaler.fit(data)
        data = scaler_model.transform(data)
        model = kmeans.fit(data)

        self.last_centroids = model.clusterCenters()
        self.last_clustered_data = model.transform(data)
