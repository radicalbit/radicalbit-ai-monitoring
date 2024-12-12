from pydantic import BaseModel, confloat
from typing import List


class Prob(BaseModel):
    id: str
    token: str
    prob: confloat(ge=0, le=1)


class MeanPerPhrase(BaseModel):
    id: str
    prob_per_phrase: confloat(ge=0, le=1)
    perplex_per_phrase: confloat(ge=1)


class MeanPerFile(BaseModel):
    prob_tot_mean: confloat(ge=0, le=1)
    perplex_tot_mean: confloat(ge=1)


class LLMMetricsModel(BaseModel):
    prob: List[Prob]
    mean_per_phrase: List[MeanPerPhrase]
    mean_per_file: List[MeanPerFile]
