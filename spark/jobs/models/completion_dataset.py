from pydantic import BaseModel, confloat, ConfigDict
from typing import List


class Prob(BaseModel):
    token: str
    prob: confloat(ge=0, le=1)


class Probs(BaseModel):
    id: str
    probs: List[Prob]

    model_config = ConfigDict(ser_json_inf_nan="null")


class MeanPerPhrase(BaseModel):
    id: str
    prob_per_phrase: confloat(ge=0, le=1)
    perplex_per_phrase: confloat(ge=1)

    model_config = ConfigDict(ser_json_inf_nan="null")


class MeanPerFile(BaseModel):
    prob_tot_mean: confloat(ge=0, le=1)
    perplex_tot_mean: confloat(ge=1)

    model_config = ConfigDict(ser_json_inf_nan="null")


class LLMMetricsModel(BaseModel):
    tokens: List[Probs]
    mean_per_phrase: List[MeanPerPhrase]
    mean_per_file: List[MeanPerFile]
