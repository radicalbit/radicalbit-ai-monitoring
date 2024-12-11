from typing import Dict, List, Optional

from pydantic import BaseModel, model_validator


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


class Response(BaseModel):
    id: str
    choices: List[Choice]
    created: int
    model: str
    object: str
    system_fingerprint: str
    usage: Usage


class CompletionResponses(BaseModel):
    responses: List[Response]

    @model_validator(mode='before')
    @classmethod
    def handle_single_response(cls, values):
        if 'responses' not in values:
            return {'responses': [values]}
        return values

    @model_validator(mode='after')
    def validate_responses_non_empty(self):
        if not self.responses or len(self.responses) == 0:
            raise ValueError(
                "The 'responses' array must contain at least one response."
            )
        return self
