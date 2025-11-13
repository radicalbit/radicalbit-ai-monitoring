from functools import reduce
from operator import add

from models.current_dataset import CurrentDataset
from models.reference_dataset import ReferenceDataset
from models.statistics import Statistics
import pyspark.sql.functions as F

N_VARIABLES = 'n_variables'
N_OBSERVATION = 'n_observations'
MISSING_CELLS = 'missing_cells'
MISSING_CELLS_PERC = 'missing_cells_perc'
DUPLICATE_ROWS = 'duplicate_rows'
DUPLICATE_ROWS_PERC = 'duplicate_rows_perc'
NUMERIC = 'numeric'
CATEGORICAL = 'categorical'
DATETIME = 'datetime'


def _calculate_statistics(
    dataframe,
    dataframe_columns,
    dataframe_dtypes,
    timestamp_column_name,
    number_of_variables,
    number_of_observations,
    number_of_numerical,
    number_of_categorical,
    number_of_datetime,
):
    # Pre-calculate columns for deduplication
    dedup_columns = [c for c in dataframe_columns if c != timestamp_column_name]

    # Calculate unique count separately to avoid nested Spark job in F.lit()
    unique_count = dataframe.dropDuplicates(dedup_columns).count()
    duplicate_count = number_of_observations - unique_count

    # Build missing cell count expressions
    missing_count_exprs = [
        F.count(F.when(F.isnan(c) | F.col(c).isNull(), c)).alias(c)
        if t not in ('datetime', 'date', 'timestamp', 'bool', 'boolean')
        else F.count(F.when(F.col(c).isNull(), c)).alias(c)
        for c, t in dataframe_dtypes
    ]

    # Use reduce for efficient column summing
    missing_cells_sum = reduce(add, [F.col(c) for c in dataframe_columns])

    stats = (
        dataframe.select(missing_count_exprs)
        .withColumn(MISSING_CELLS, missing_cells_sum)
        .withColumn(
            MISSING_CELLS_PERC,
            (F.col(MISSING_CELLS) / (number_of_variables * number_of_observations))
            * 100,
        )
        .withColumn(DUPLICATE_ROWS, F.lit(duplicate_count))
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
            MISSING_CELLS,
            MISSING_CELLS_PERC,
            DUPLICATE_ROWS,
            DUPLICATE_ROWS_PERC,
            N_VARIABLES,
            N_OBSERVATION,
            NUMERIC,
            CATEGORICAL,
            DATETIME,
        )
    )

    # Direct conversion without pandas overhead
    stats_dict = stats.first().asDict()

    return Statistics(**stats_dict)


# FIXME use pydantic struct like data quality
# FIXME generalize to one method
def calculate_statistics_reference(
    reference_dataset: ReferenceDataset,
) -> Statistics:
    number_of_variables = len(reference_dataset.get_all_variables())
    number_of_observations = reference_dataset.reference_count
    number_of_numerical = len(reference_dataset.get_numerical_variables())
    number_of_categorical = len(reference_dataset.get_categorical_variables())
    number_of_datetime = len(reference_dataset.get_datetime_variables())

    return _calculate_statistics(
        dataframe=reference_dataset.reference,
        dataframe_columns=reference_dataset.reference.columns,
        dataframe_dtypes=reference_dataset.reference.dtypes,
        timestamp_column_name=reference_dataset.model.timestamp.name,
        number_of_variables=number_of_variables,
        number_of_observations=number_of_observations,
        number_of_numerical=number_of_numerical,
        number_of_categorical=number_of_categorical,
        number_of_datetime=number_of_datetime,
    )


def calculate_statistics_current(
    current_dataset: CurrentDataset,
) -> Statistics:
    number_of_variables = len(current_dataset.get_all_variables())
    number_of_observations = current_dataset.current_count
    number_of_numerical = len(current_dataset.get_numerical_variables())
    number_of_categorical = len(current_dataset.get_categorical_variables())
    number_of_datetime = len(current_dataset.get_datetime_variables())

    return _calculate_statistics(
        dataframe=current_dataset.current,
        dataframe_columns=current_dataset.current.columns,
        dataframe_dtypes=current_dataset.current.dtypes,
        timestamp_column_name=current_dataset.model.timestamp.name,
        number_of_variables=number_of_variables,
        number_of_observations=number_of_observations,
        number_of_numerical=number_of_numerical,
        number_of_categorical=number_of_categorical,
        number_of_datetime=number_of_datetime,
    )
