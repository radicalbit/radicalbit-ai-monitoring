import logging
from typing import Any, Dict, List, Tuple

import numpy as np
from pyspark.ml.clustering import KMeans
from pyspark.ml.evaluation import ClusteringEvaluator
from pyspark.ml.feature import PCA, StandardScaler, VectorAssembler
from pyspark.ml.linalg import Vectors, VectorUDT
from pyspark.sql import DataFrame, SparkSession, functions as f

logger = logging.getLogger(__name__)


class EmbeddingsDriftDetector:
    def __init__(self, embeddings, prefix_id, variance_threshold):
        self.embeddings = embeddings
        self.column_names = self.embeddings.columns
        self.prefix_id = prefix_id
        self.variance_threshold = variance_threshold

    def compute_centroid(self) -> DataFrame:
        aggregation_expressions = [f.mean(c).alias(c) for c in self.column_names]
        centroid_df = self.embeddings.agg(*aggregation_expressions)
        return centroid_df


    def compute_distance(self) -> List[float]:
        """Computes the Euclidean distance between each embedding row and the centroid.
        """

        distance_column_name = f'{self.prefix_id}_euclidean_distance'

        embedding_centroid_df = self.compute_centroid()

        # Collect the centroid to the driver.
        centroid_row = embedding_centroid_df.first()

        # Add error handling in case the centroid computation is empty
        if centroid_row is None:
            raise ValueError(
                'Centroid computation returned no result. Cannot compute distance.'
            )

        squared_diffs_exprs = [
            f.pow(f.col(c) - f.lit(centroid_row[c]), 2) for c in self.column_names
        ]
        # Check if the list is empty before summing
        if not squared_diffs_exprs:
            # Handle case of no columns - maybe return df with distance 0 or None
            return self.embeddings.withColumn(distance_column_name, f.lit(0.0))

        sum_sq_diff_expr = sum(squared_diffs_exprs, start=f.lit(0.0))

        # Add the distance column to the DataFrame
        df_with_distance = self.embeddings.withColumn(
            distance_column_name,
            f.sqrt(sum_sq_diff_expr),  # Take the square root of the sum
        ).select(distance_column_name)

        return [row[f'{distance_column_name}'] for row in df_with_distance.collect()]

    def scale_embeddings(self) -> DataFrame:
        assembler = VectorAssembler(
            inputCols=self.column_names, outputCol='raw_features'
        )
        df_assembled = assembler.transform(self.embeddings)

        scaler = StandardScaler(
            inputCol='raw_features',
            outputCol='scaled_features',
            withStd=True,
            withMean=True,
        )
        scaler_model = scaler.fit(df_assembled)
        df_scaled = scaler_model.transform(df_assembled)

        return df_scaled.select('scaled_features')

    def find_k_optimal_components(self, scaled_df: DataFrame) -> int:
        # fit pca with the max possible dimension
        pca_initial = PCA(
            k=len(self.column_names),
            inputCol='scaled_features',
            outputCol='pca_temp_features',
        )
        pca_initial_model = pca_initial.fit(scaled_df)

        explained_variance_ratio = pca_initial_model.explainedVariance.toArray()
        cumulative_variance = np.cumsum(explained_variance_ratio)

        k_optimal_components = (
            np.argmax(cumulative_variance >= self.variance_threshold) + 1
        )

        return k_optimal_components

    def compute_pca_df(self, scaled_df: DataFrame, n_components: int) -> DataFrame:
        pca_final = PCA(
            k=n_components, inputCol='scaled_features', outputCol='pca_features'
        )
        pca_final_model = pca_final.fit(scaled_df)
        df_pca_final = pca_final_model.transform(scaled_df)

        return df_pca_final.select(['pca_features'])

    def find_optimal_clusters_number(self, reduced_df) -> Tuple[int, Dict[int, float]]:
        k_min = 2
        k_max = 4 #int(np.floor(len(self.column_names) / 3))
        k_values = range(k_min, k_max + 1)

        pca_features_col = 'pca_features'

        silhouette_scores = {}
        for k in k_values:
            print(f'Finding optimal cluster number - processing k: {k}')
            kmeans = KMeans(
                featuresCol=pca_features_col, k=k, seed=42, predictionCol='prediction'
            )
            model = kmeans.fit(reduced_df)
            predictions = model.transform(reduced_df)

            evaluator = ClusteringEvaluator(
                featuresCol=pca_features_col,
                predictionCol='prediction',  # Must match KMeans output predictionCol
                metricName='silhouette',
                distanceMeasure='squaredEuclidean',
            )

            score = evaluator.evaluate(predictions)
            silhouette_scores[k] = score

        optimal_clusters_number = max(silhouette_scores, key=silhouette_scores.get)

        return optimal_clusters_number, silhouette_scores

    def compute_final_kmeans(self, reduced_df: DataFrame, k_clusters: int) -> Tuple[float, float]:
        pca_features_col = 'pca_features'

        kmeans = KMeans(
            featuresCol=pca_features_col,
            k=k_clusters,
            seed=42,
            predictionCol='prediction',
        )
        model = kmeans.fit(reduced_df)
        predictions = model.transform(reduced_df)

        evaluator = ClusteringEvaluator(
            featuresCol=pca_features_col,
            predictionCol='prediction',  # Must match KMeans output predictionCol
            metricName='silhouette',
            distanceMeasure='squaredEuclidean',
        )

        # Calculate the Silhouette score
        # Note: Silhouette score computation in Spark can be computationally intensive!
        silhouette_scores = evaluator.evaluate(predictions)

        inertia_scores = model.summary.trainingCost

        return silhouette_scores, inertia_scores

    def compute_result(self):
        #  ---  Process ---
        # step 1: scale data
        scaled_df = self.scale_embeddings()


        # step 2: find optimal components number
        optimal_components_number = self.find_k_optimal_components(scaled_df=scaled_df)

        # step 3: compute pca with optimal components number
        optimal_pca = self.compute_pca_df(
            scaled_df=scaled_df, n_components=optimal_components_number
        )

        # step 4: find optimal clusters number
        optimal_clusters_number, silhouette_scores_tmp = (
            self.find_optimal_clusters_number(reduced_df=optimal_pca)
        )

        # step 5: train final kmeans
        final_silhouette_score, inertia_score = self.compute_final_kmeans(
            reduced_df=optimal_pca, k_clusters=optimal_clusters_number
        )


        #  --- Visualisation info ---
        # distances
        centroid_embeddings_distance = self.compute_distance()
        return centroid_embeddings_distance

        #
        # # 2d scatterplot
        # def select_first_two_components(vector):
        #     if vector is not None and hasattr(vector, 'size') and vector.size >= 2:
        #         return Vectors.dense([vector[0], vector[1]])
        #     else:
        #         return None
        #
        # select_first_two_udf = f.udf(select_first_two_components, VectorUDT())
        #
        # two_d_pca = optimal_pca.withColumn(
        #     'first_two_pca', select_first_two_udf(f.col('pca_features'))
        # ).select('first_two_pca')
        #
        # x_y_pca = [
        #     [row.first_two_pca[0], row.first_two_pca[1]] for row in two_d_pca.collect()
        # ]
        #
        # # find 2d centroid
        # x_y_centroid = [
        #     [np.mean([coord[0] for coord in x_y_pca])],
        #     [np.mean([coord[1] for coord in x_y_pca])],
        # ]
        #
        # return {
        #     'table': {
        #         'number_of_optimal_components': optimal_components_number,
        #         'number_of_optimal_clusters': optimal_clusters_number,
        #         'silhouette_score': final_silhouette_score,
        #         'inertia': inertia_score,
        #     },
        #     'barplot': {'distances': centroid_embeddings_distance},
        #     'scatterplot': {'x_y_coordinates': x_y_pca, 'x_y_centroid': x_y_centroid},
        # }


import pandas as pd


def main():
    np.random.seed(1990)
    # spark session
    spark = SparkSession.builder.appName('Drift-Emb').getOrCreate()

    size = 60
    emb_df = pd.DataFrame([np.random.uniform(size=1536) for _ in range(size)])
    #emb_df = pd.read_csv("../../Downloads/embeddings.csv")
    print(emb_df.shape)

    emb_spark = spark.createDataFrame(emb_df)

    print('raw df')
    print(emb_spark.show())

    dd = EmbeddingsDriftDetector(
        embeddings=emb_spark, prefix_id='mauro', variance_threshold=0.80
    )

    res = dd.compute_result()

    print(res)

    # print(res)


if __name__ == '__main__':
    main()
