from pydantic import BaseModel, ConfigDict

from typing import Optional


class Statistics(BaseModel):
    n_variables: int
    n_observations: int
    missing_cells: int
    missing_cells_perc: Optional[float]
    duplicate_rows: int
    duplicate_rows_perc: Optional[float]
    numeric: int
    categorical: int
    datetime: int

    model_config = ConfigDict(ser_json_inf_nan="null")
