from pydantic import BaseModel, confloat, ConfigDict
from typing import List


class Prob(BaseModel):
    token: str
    prob: confloat(ge=0, le=1)


class Probs(BaseModel):
    id: str
    message_content: str
    probs: List[Prob]
    rbit_timestamp: str
    model_name: str
    total_token: int
    perplexity: confloat(ge=1)
    probability: confloat(ge=0, le=1)

    model_config = ConfigDict(ser_json_inf_nan="null")


class MeanPerFile(BaseModel):
    prob_tot_mean: confloat(ge=0, le=1)
    perplex_tot_mean: confloat(ge=1)

    model_config = ConfigDict(ser_json_inf_nan="null")


class CompletionMetricsModel(BaseModel):
    tokens: List[Probs]
    mean_per_file: List[MeanPerFile]
