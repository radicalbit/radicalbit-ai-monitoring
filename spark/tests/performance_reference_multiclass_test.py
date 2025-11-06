"""Performance test to demonstrate the efficiency of reference multiclass metrics calculation.

Run with: pytest tests/performance_reference_multiclass_test.py -v -s

This test generates a large reference dataset to showcase
the performance of the optimized reference metrics calculation.
"""

import datetime
import random
import uuid

from models.current_dataset import CurrentDataset
from models.reference_dataset import ReferenceDataset
from pyspark.sql import Row
import pytest
from utils.reference_multiclass import ReferenceMetricsMulticlassService

from jobs.utils.models import (
    ColumnDefinition,
    DataType,
    FieldTypes,
    Granularity,
    ModelOut,
    ModelType,
    OutputType,
    SupportedTypes,
)
from tests.utils.pytest_utils import prefix_id


@pytest.fixture
def large_reference_dataset_for_performance(spark_fixture):
    """Generate a large reference dataset with:
    - 10,000 rows
    - 5 classes
    - 4 features

    This will test the efficiency of reference metrics calculation with large data.
    """
    random.seed(42)

    classes = ['CLASS_A', 'CLASS_B', 'CLASS_C', 'CLASS_D', 'CLASS_E']
    cat1_values = ['X', 'Y', 'Z']
    cat2_values = ['P', 'Q', 'R']

    # Base datetime
    base_dt = datetime.datetime(2024, 6, 1, 0, 0, 0)

    # Generate reference data (10,000 rows)
    reference_data = []
    rows_per_class = 2000  # 2000 rows per class

    for cls in classes:
        for _ in range(rows_per_class):
            reference_data.append(
                Row(
                    cat1=random.choice(cat1_values),
                    cat2=random.choice(cat2_values),
                    num1=round(random.uniform(0.0, 100.0), 2),
                    num2=round(random.uniform(0.0, 500.0), 2),
                    prediction=cls,
                    target=cls,
                    datetime=str(
                        base_dt + datetime.timedelta(hours=random.randint(0, 99))
                    ),
                )
            )

    # Generate current data (small, just needs one row per class)
    current_data = []
    for i, cls in enumerate(classes):
        current_data.append(
            Row(
                cat1=random.choice(cat1_values),
                cat2=random.choice(cat2_values),
                num1=round(random.uniform(0.0, 100.0), 2),
                num2=round(random.uniform(0.0, 500.0), 2),
                prediction=cls,
                target=cls,
                datetime=str(base_dt + datetime.timedelta(hours=i)),
            )
        )

    reference_df = spark_fixture.createDataFrame(reference_data)
    current_df = spark_fixture.createDataFrame(current_data)

    return reference_df, current_df


def test_performance_large_reference_dataset(
    spark_fixture, large_reference_dataset_for_performance
):
    """Performance test with a large reference dataset.

    Expected behavior:
    - OPTIMIZED CODE: Efficient calculation with batched computation
    """
    output = OutputType(
        prediction=ColumnDefinition(
            name='prediction',
            type=SupportedTypes.string,
            field_type=FieldTypes.categorical,
        ),
        prediction_proba=None,
        output=[
            ColumnDefinition(
                name='prediction',
                type=SupportedTypes.string,
                field_type=FieldTypes.categorical,
            )
        ],
    )
    target = ColumnDefinition(
        name='target', type=SupportedTypes.string, field_type=FieldTypes.categorical
    )
    timestamp = ColumnDefinition(
        name='datetime', type=SupportedTypes.datetime, field_type=FieldTypes.datetime
    )
    granularity = Granularity.HOUR
    features = [
        ColumnDefinition(
            name='cat1', type=SupportedTypes.string, field_type=FieldTypes.categorical
        ),
        ColumnDefinition(
            name='cat2', type=SupportedTypes.string, field_type=FieldTypes.categorical
        ),
        ColumnDefinition(
            name='num1', type=SupportedTypes.float, field_type=FieldTypes.numerical
        ),
        ColumnDefinition(
            name='num2', type=SupportedTypes.float, field_type=FieldTypes.numerical
        ),
    ]
    model = ModelOut(
        uuid=uuid.uuid4(),
        name='performance_test_model_reference',
        description='Performance test for reference multiclass metrics',
        model_type=ModelType.MULTI_CLASS,
        data_type=DataType.TABULAR,
        timestamp=timestamp,
        granularity=granularity,
        outputs=output,
        target=target,
        features=features,
        frameworks='framework',
        algorithm='algorithm',
        created_at=str(datetime.datetime.now()),
        updated_at=str(datetime.datetime.now()),
    )

    reference_dataframe, current_dataframe = large_reference_dataset_for_performance
    current_dataset = CurrentDataset(
        model=model, raw_dataframe=current_dataframe, prefix_id=prefix_id
    )
    reference_dataset = ReferenceDataset(
        model=model, raw_dataframe=reference_dataframe, prefix_id=prefix_id
    )

    metrics_service = ReferenceMetricsMulticlassService(
        reference=reference_dataset,
        prefix_id=prefix_id,
    )

    model_quality = metrics_service.calculate_model_quality()

    # Basic validation
    assert model_quality is not None
    assert 'classes' in model_quality
    assert 'class_metrics' in model_quality
    assert 'global_metrics' in model_quality
    assert len(model_quality['classes']) == 5
