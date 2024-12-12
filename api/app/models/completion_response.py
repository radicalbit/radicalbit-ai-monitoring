from typing import Dict, List, Optional

from pydantic import BaseModel, RootModel, model_validator


class TokenLogProbs(BaseModel):
    token: str
    bytes: List[int]
    logprob: float
    top_logprobs: List[Dict[str, float]]


class LogProbs(BaseModel):
    content: List[TokenLogProbs]
    refusal: Optional[str] = None


class Message(BaseModel):
    content: str
    refusal: Optional[str] = None
    role: str
    tool_calls: List = []
    parsed: Optional[dict] = None


class Choice(BaseModel):
    finish_reason: str
    index: int
    logprobs: Optional[LogProbs] = None
    message: Message

    @model_validator(mode='after')
    def validate_logprobs(self):
        if self.logprobs is None:
            raise ValueError(
                "the 'logprobs' field cannot be empty, metrics could not be computed."
            )
        return self


class UsageDetails(BaseModel):
    accepted_prediction_tokens: int = 0
    reasoning_tokens: int = 0
    rejected_prediction_tokens: int = 0
    audio_tokens: Optional[int] = None
    cached_tokens: Optional[int] = None


class Usage(BaseModel):
    completion_tokens: int
    prompt_tokens: int
    total_tokens: int
    completion_tokens_details: UsageDetails
    prompt_tokens_details: Optional[UsageDetails] = None


class Completion(BaseModel):
    id: str
    choices: List[Choice]
    created: int
    model: str
    object: str
    system_fingerprint: str
    usage: Usage


class CompletionResponses(RootModel[List[Completion]]):
    @model_validator(mode='before')
    @classmethod
    def handle_single_completion(cls, data):
        """If a single object is passed instead of a list, wrap it into a list."""
        if isinstance(data, dict):
            return [data]
        if isinstance(data, list):
            return data
        raise ValueError(
            'Input file must be a list of completion json or a single completion json'
        )
