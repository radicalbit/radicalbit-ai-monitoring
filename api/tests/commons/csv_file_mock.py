# Mock csv data as file object
from io import BytesIO, StringIO

from fastapi import UploadFile
import pandas as pd

from app.models.inferred_schema_dto import (
    FieldType,
    InferredSchemaDTO,
    SchemaEntry,
    SupportedTypes,
)


def get_dataframe() -> pd.DataFrame:
    return get_dataframe_with_sep(',')


def get_dataframe_with_sep(sep: str) -> pd.DataFrame:
    data = StringIO(
        f"""
    Name{sep}Age{sep}City{sep}Salary{sep}String{sep}Float/Int{sep}Boolean{sep}Datetime{sep}Datetime2{sep}Datetime3
    John Doe{sep}25{sep}New York{sep}50000.50{sep}Data 1{sep}123{sep}True{sep}2024-06-06 12:05:56{sep}2024-06-06T13:40:27{sep}06/06/2024 13:40:27
    Jane Smith{sep}30{sep}London{sep}60000.75{sep}Data 2{sep}456.789{sep}False{sep}2024-06-06 12:07:36{sep}2024-06-06T13:40:27{sep}06/06/2024 13:40:27
    """.strip()
    )
    return pd.read_csv(data, sep=sep)


def correct_schema() -> InferredSchemaDTO:
    schema = [
        {
            'name': 'Name',
            'type': SupportedTypes.string,
            'fieldType': FieldType.categorical,
        },
        {'name': 'Age', 'type': SupportedTypes.int, 'fieldType': FieldType.numerical},
        {
            'name': 'City',
            'type': SupportedTypes.string,
            'fieldType': FieldType.categorical,
        },
        {
            'name': 'Salary',
            'type': SupportedTypes.float,
            'fieldType': FieldType.numerical,
        },
        {
            'name': 'String',
            'type': SupportedTypes.string,
            'fieldType': FieldType.categorical,
        },
        {
            'name': 'Float/Int',
            'type': SupportedTypes.float,
            'fieldType': FieldType.numerical,
        },
        {
            'name': 'Boolean',
            'type': SupportedTypes.bool,
            'fieldType': FieldType.categorical,
        },
        {
            'name': 'Datetime',
            'type': SupportedTypes.datetime,
            'fieldType': FieldType.datetime,
        },
        {
            'name': 'Datetime2',
            'type': SupportedTypes.datetime,
            'fieldType': FieldType.datetime,
        },
        {
            'name': 'Datetime3',
            'type': SupportedTypes.datetime,
            'fieldType': FieldType.datetime,
        },
    ]
    schema = [SchemaEntry(**entry) for entry in schema]
    return InferredSchemaDTO(inferred_schema=schema)


def get_correct_sample_csv_file() -> UploadFile:
    df = get_dataframe()
    return UploadFile(BytesIO(df.to_csv(index=False).encode()), filename='sample.csv')


def get_uncorrect_sample_csv_file() -> UploadFile:
    df = get_dataframe()
    return UploadFile(BytesIO(df.to_csv(index=False).encode()), filename=None)


def get_file_using_sep(sep: str) -> UploadFile:
    df = get_dataframe_with_sep(sep)
    return UploadFile(
        BytesIO(df.to_csv(index=False, sep=sep).encode()), filename='sample.csv'
    )


def get_current_sample_csv_file() -> UploadFile:
    data = StringIO(
        """
            id,cat1,cat2,num1,num2,prediction,prediction_proba,target,datetime
            1,A,A,1,100,1,1,1,2024-06-16 00:01:00-05:00
            2,B,B,1,100,1,1,1,2024-06-16 00:02:00-05:00
            3,C,C,1,100,1,1,1,2024-06-16 00:03:00-05:00
            4,D,D,1,100,1,1,1,2024-06-16 00:04:00-05:00
            5,E,E,1,100,1,1,1,2024-06-16 00:05:00-05:00
            6,F,F,1,100,1,1,1,2024-06-16 00:06:00-05:00
            7,G,G,1,100,1,1,1,2024-06-16 00:07:00-05:00
        """.strip()
    )
    df = pd.read_csv(data, sep=',')
    return UploadFile(BytesIO(df.to_csv(index=False).encode()), filename='sample.csv')
