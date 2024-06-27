import pyspark.sql.functions as F


def apply_schema_to_dataframe(df, schema):
    for field in schema.fields:
        df = df.withColumn(field.name, F.col(field.name).cast(field.dataType))
    return df


def check_not_null(x):
    return F.when(F.col(x).isNotNull() & ~F.isnan(x), F.col(x))
