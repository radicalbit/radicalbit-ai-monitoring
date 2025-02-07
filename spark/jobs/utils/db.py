import os
from typing import Dict

from pyspark.sql import SparkSession
from pyspark.sql.types import StructType

import psycopg2

# TODO Define connection details in a better way, this comes from env secrets
db_host = os.getenv("POSTGRES_HOST")
db_port = os.getenv("POSTGRES_PORT")
db_name = os.getenv("POSTGRES_DB")
user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
postgres_schema = os.getenv("POSTGRES_SCHEMA")

url = f"jdbc:postgresql://{db_host}:{db_port}/{db_name}"


def update_job_status(file_uuid: str, status: str, dataset_table_name: str):
    # Use psycopg2 to update the job status
    with psycopg2.connect(
        host=db_host,
        dbname=db_name,
        user=user,
        password=password,
        port=db_port,
        options=f"-c search_path=dbo,{postgres_schema}",
    ) as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"""
                UPDATE {dataset_table_name}
                SET "STATUS" = %s
                WHERE "UUID" = %s
                """,
                (status, file_uuid),
            )
            conn.commit()

def write_to_db(
    spark_session: SparkSession,
    record: Dict,
    schema: StructType,
    metrics_table_name: str,
):
    out_df = spark_session.createDataFrame(data=[record], schema=schema)

    # stringtype is needed for jsonb
    out_df.write.format("jdbc").option("url", url).option(
        "stringtype", "unspecified"
    ).option("driver", "org.postgresql.Driver").option("user", user).option(
        "password", password
    ).option("dbtable", f'"{postgres_schema}"."{metrics_table_name}"').mode(
        "append"
    ).save()
