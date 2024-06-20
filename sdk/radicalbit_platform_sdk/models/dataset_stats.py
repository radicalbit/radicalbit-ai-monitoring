from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class DatasetStats(BaseModel):
    n_variables: int
    n_observations: int
    missing_cells: int
    missing_cells_perc: float
    duplicate_rows: int
    duplicate_rows_perc: float
    numeric: int
    categorical: int
    datetime: int

    model_config = ConfigDict(
        populate_by_name=True, alias_generator=to_camel, protected_namespaces=()
    )
