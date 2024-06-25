from pyspark.sql import DataFrame

from ..utils.models import ModelOut
from ..utils.spark import apply_schema_to_dataframe


class ReferenceDataset:

    def __init__(self, model: ModelOut, raw_dataframe: DataFrame):
        reference_schema = model.to_reference_spark_schema()
        reference_dataset = apply_schema_to_dataframe(raw_dataframe, reference_schema)

        self.model = model
        self.reference = reference_dataset.select(
            *[c for c in reference_schema.names if c in reference_dataset.columns]
        )
        self.reference_count = self.reference.count()
