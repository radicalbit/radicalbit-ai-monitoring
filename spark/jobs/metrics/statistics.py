from models.current_dataset import CurrentDataset
from models.reference_dataset import ReferenceDataset
import pyspark.sql.functions as F

N_VARIABLES = "n_variables"
N_OBSERVATION = "n_observations"
MISSING_CELLS = "missing_cells"
MISSING_CELLS_PERC = "missing_cells_perc"
DUPLICATE_ROWS = "duplicate_rows"
DUPLICATE_ROWS_PERC = "duplicate_rows_perc"
NUMERIC = "numeric"
CATEGORICAL = "categorical"
DATETIME = "datetime"


# FIXME use pydantic struct like data quality
def calculate_statistics_reference(
    reference_dataset: ReferenceDataset,
) -> dict[str, float]:
    number_of_variables = len(reference_dataset.get_all_variables())
    number_of_observations = reference_dataset.reference_count
    number_of_numerical = len(reference_dataset.get_numerical_variables())
    number_of_categorical = len(reference_dataset.get_categorical_variables())
    number_of_datetime = len(reference_dataset.get_datetime_variables())
    reference_columns = reference_dataset.reference.columns

    stats = (
        reference_dataset.reference.select(
            [
                F.count(F.when(F.isnan(c) | F.col(c).isNull(), c)).alias(c)
                if t not in ("datetime", "date", "timestamp", "bool", "boolean")
                else F.count(F.when(F.col(c).isNull(), c)).alias(c)
                for c, t in reference_dataset.reference.dtypes
            ]
        )
        .withColumn(MISSING_CELLS, sum([F.col(c) for c in reference_columns]))
        .withColumn(
            MISSING_CELLS_PERC,
            (F.col(MISSING_CELLS) / (number_of_variables * number_of_observations))
            * 100,
        )
        .withColumn(
            DUPLICATE_ROWS,
            F.lit(
                number_of_observations
                - reference_dataset.reference.dropDuplicates(
                    [
                        c
                        for c in reference_columns
                        if c != reference_dataset.model.timestamp.name
                    ]
                ).count()
            ),
        )
        .withColumn(
            DUPLICATE_ROWS_PERC,
            (F.col(DUPLICATE_ROWS) / number_of_observations) * 100,
        )
        .withColumn(N_VARIABLES, F.lit(number_of_variables))
        .withColumn(N_OBSERVATION, F.lit(number_of_observations))
        .withColumn(NUMERIC, F.lit(number_of_numerical))
        .withColumn(CATEGORICAL, F.lit(number_of_categorical))
        .withColumn(DATETIME, F.lit(number_of_datetime))
        .select(
            *[
                MISSING_CELLS,
                MISSING_CELLS_PERC,
                DUPLICATE_ROWS,
                DUPLICATE_ROWS_PERC,
                N_VARIABLES,
                N_OBSERVATION,
                NUMERIC,
                CATEGORICAL,
                DATETIME,
            ]
        )
        .toPandas()
        .to_dict(orient="records")[0]
    )

    return stats


def calculate_statistics_current(
    current_dataset: CurrentDataset,
) -> dict[str, float]:
    number_of_variables = len(current_dataset.get_all_variables())
    number_of_observations = current_dataset.current_count
    number_of_numerical = len(current_dataset.get_numerical_variables())
    number_of_categorical = len(current_dataset.get_categorical_variables())
    number_of_datetime = len(current_dataset.get_datetime_variables())
    reference_columns = current_dataset.current.columns

    stats = (
        current_dataset.current.select(
            [
                F.count(F.when(F.isnan(c) | F.col(c).isNull(), c)).alias(c)
                if t not in ("datetime", "date", "timestamp", "bool", "boolean")
                else F.count(F.when(F.col(c).isNull(), c)).alias(c)
                for c, t in current_dataset.current.dtypes
            ]
        )
        .withColumn(MISSING_CELLS, sum([F.col(c) for c in reference_columns]))
        .withColumn(
            MISSING_CELLS_PERC,
            (F.col(MISSING_CELLS) / (number_of_variables * number_of_observations))
            * 100,
        )
        .withColumn(
            DUPLICATE_ROWS,
            F.lit(
                number_of_observations
                - current_dataset.current.dropDuplicates(
                    [
                        c
                        for c in reference_columns
                        if c != current_dataset.model.timestamp.name
                    ]
                ).count()
            ),
        )
        .withColumn(
            DUPLICATE_ROWS_PERC,
            (F.col(DUPLICATE_ROWS) / number_of_observations) * 100,
        )
        .withColumn(N_VARIABLES, F.lit(number_of_variables))
        .withColumn(N_OBSERVATION, F.lit(number_of_observations))
        .withColumn(NUMERIC, F.lit(number_of_numerical))
        .withColumn(CATEGORICAL, F.lit(number_of_categorical))
        .withColumn(DATETIME, F.lit(number_of_datetime))
        .select(
            *[
                MISSING_CELLS,
                MISSING_CELLS_PERC,
                DUPLICATE_ROWS,
                DUPLICATE_ROWS_PERC,
                N_VARIABLES,
                N_OBSERVATION,
                NUMERIC,
                CATEGORICAL,
                DATETIME,
            ]
        )
        .toPandas()
        .to_dict(orient="records")[0]
    )

    return stats
