from typing import Dict, List, Tuple

import numpy as np
from pyspark.ml.clustering import KMeans
from pyspark.ml.evaluation import ClusteringEvaluator
from pyspark.ml.feature import PCA, StandardScaler, VectorAssembler
from pyspark.ml.linalg import Vectors, VectorUDT
from pyspark.sql import DataFrame, functions as f
from pyspark.sql.types import DoubleType

# from utils.logger import logger_config

# logger = logging.getLogger(logger_config.get('logger_name', 'default'))


class EmbeddingsDriftDetector:
    def __init__(self, spark, embeddings, prefix_id, variance_threshold):
        self.spark = spark
        self.embeddings = embeddings
        self.column_names = self.embeddings.columns
        self.prefix_id = prefix_id
        self.variance_threshold = variance_threshold

    def compute_centroid(self) -> List[float]:
        """Compute the centroid and returns it as a Python list."""
        aggregation_expressions = [f.mean(c).alias(c) for c in self.column_names]
        centroid_row = self.embeddings.agg(*aggregation_expressions).first()

        if centroid_row is None:
            raise ValueError('Centroid computation returned no result.')

        # Return centroid as a list, maintaining order
        return [centroid_row[c] for c in self.column_names]

    def compute_distance(self) -> List[float]:
        """Compute the Euclidean distance between each embedding row and the centroid using a UDF."""

        distance_column_name = f'{self.prefix_id}_euclidean_distance'

        centroid_list = self.compute_centroid()

        # This sends the centroid array to each executor node only once.
        broadcasted_centroid = self.spark.sparkContext.broadcast(centroid_list)

        # Define the UDF
        @f.udf(returnType=DoubleType())
        def euclidean_distance_udf(*embedding_vector_cols):
            centroid_val = broadcasted_centroid.value  # Access the broadcasted value
            diff = np.array(embedding_vector_cols) - np.array(centroid_val)
            return float(np.sqrt(np.sum(diff**2)))

        # Apply the UDF
        df_with_distance = self.embeddings.withColumn(
            distance_column_name,
            euclidean_distance_udf(
                *[f.col(c) for c in self.column_names]
            ),  # Unpack columns as arguments
        ).select(distance_column_name)

        # Collect the results
        return [float(row[distance_column_name]) for row in df_with_distance.collect()]

    def scale_embeddings(self) -> DataFrame:
        assembler = VectorAssembler(
            inputCols=self.column_names, outputCol=f'{self.prefix_id}_raw_features'
        )
        df_assembled = assembler.transform(self.embeddings)

        scaler = StandardScaler(
            inputCol=f'{self.prefix_id}_raw_features',
            outputCol=f'{self.prefix_id}_scaled_features',
            withStd=True,
            withMean=True,
        )
        scaler_model = scaler.fit(df_assembled)
        df_scaled = scaler_model.transform(df_assembled)

        return df_scaled.select(f'{self.prefix_id}_scaled_features')

    def find_k_optimal_components(self, scaled_df: DataFrame) -> int:
        # fit pca with the max possible dimension
        pca_initial = PCA(
            k=len(self.column_names),
            inputCol=f'{self.prefix_id}_scaled_features',
            outputCol=f'{self.prefix_id}_pca_temp_features',
        )
        pca_initial_model = pca_initial.fit(scaled_df)

        explained_variance_ratio = pca_initial_model.explainedVariance.toArray()
        cumulative_variance = np.cumsum(explained_variance_ratio)
        return int(np.argmax(cumulative_variance >= self.variance_threshold) + 1)

    def compute_pca_df(self, scaled_df: DataFrame, n_components: int) -> DataFrame:
        pca_final = PCA(
            k=n_components,
            inputCol=f'{self.prefix_id}_scaled_features',
            outputCol=f'{self.prefix_id}_pca_features',
        )
        pca_final_model = pca_final.fit(scaled_df)
        df_pca_final = pca_final_model.transform(scaled_df)

        return df_pca_final.select([f'{self.prefix_id}_pca_features'])

    def find_optimal_clusters_number(self, reduced_df) -> Tuple[int, Dict[int, float]]:
        k_min = 2
        k_max = 5
        k_values = range(k_min, k_max + 1)

        pca_features_col = f'{self.prefix_id}_pca_features'

        silhouette_scores = {}
        for k in k_values:
            # logger.info('Finding optimal cluster number - processing k: %s', k)
            kmeans = KMeans(
                featuresCol=pca_features_col,
                k=k,
                seed=42,
                predictionCol=f'{self.prefix_id}_prediction',
            )
            model = kmeans.fit(reduced_df)
            predictions = model.transform(reduced_df)

            evaluator = ClusteringEvaluator(
                featuresCol=pca_features_col,
                predictionCol=f'{self.prefix_id}_prediction',  # Must match KMeans output predictionCol
                metricName='silhouette',
                distanceMeasure='squaredEuclidean',
            )

            score = evaluator.evaluate(predictions)
            silhouette_scores[k] = score

        optimal_clusters_number = max(silhouette_scores, key=silhouette_scores.get)

        return int(optimal_clusters_number), silhouette_scores

    def compute_final_kmeans(
        self, reduced_df: DataFrame, k_clusters: int
    ) -> Tuple[float, float]:
        pca_features_col = f'{self.prefix_id}_pca_features'

        kmeans = KMeans(
            featuresCol=pca_features_col,
            k=k_clusters,
            seed=42,
            predictionCol=f'{self.prefix_id}_prediction',
        )
        model = kmeans.fit(reduced_df)
        predictions = model.transform(reduced_df)

        evaluator = ClusteringEvaluator(
            featuresCol=pca_features_col,
            predictionCol=f'{self.prefix_id}_prediction',  # Must match KMeans output predictionCol
            metricName='silhouette',
            distanceMeasure='squaredEuclidean',
        )

        # Calculate the Silhouette score
        # Note: Silhouette score computation in Spark can be computationally intensive!
        silhouette_scores = evaluator.evaluate(predictions)

        inertia_scores = model.summary.trainingCost

        return float(silhouette_scores), float(inertia_scores)

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

        # 2d scatterplot
        def select_first_two_components(vector):
            if vector is not None and hasattr(vector, 'size') and vector.size >= 2:
                return Vectors.dense([vector[0], vector[1]])
            return None

        select_first_two_udf = f.udf(select_first_two_components, VectorUDT())

        two_d_pca = optimal_pca.withColumn(
            f'{self.prefix_id}_first_two_pca',
            select_first_two_udf(f.col(f'{self.prefix_id}_pca_features')),
        ).select(f'{self.prefix_id}_first_two_pca')

        x_y_pca = [
            [
                float(row[f'{self.prefix_id}_first_two_pca'][0]),
                float(row[f'{self.prefix_id}_first_two_pca'][1]),
            ]
            for row in two_d_pca.collect()
        ]

        # find 2d centroid
        x_y_centroid = [
            [float(np.mean([coord[0] for coord in x_y_pca]))],
            [float(np.mean([coord[1] for coord in x_y_pca]))],
        ]
        return {
            'table': {
                'number_of_optimal_components': optimal_components_number,
                'number_of_optimal_clusters': optimal_clusters_number,
                'silhouette_score': final_silhouette_score,
                'inertia': inertia_score,
            },
            'barplot': {'distances': centroid_embeddings_distance},
            'scatterplot': {'x_y_coordinates': x_y_pca, 'x_y_centroid': x_y_centroid},
        }
