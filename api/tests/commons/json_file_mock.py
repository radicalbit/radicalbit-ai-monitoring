from io import BytesIO

from fastapi import UploadFile


def get_completion_sample_json_file() -> UploadFile:
    json_content = """
    {
        "id": "chatcmpl-0120",
        "choices": [
            {
                "finish_reason": "stop",
                "index": 0,
                "logprobs": {
                    "content": [
                        {
                            "token": "Sky",
                            "bytes": [83, 107, 121],
                            "logprob": -1.2830728,
                            "top_logprobs": []
                        }
                    ],
                    "refusal": null
                },
                "message": {
                    "content": "Sky is blue.",
                    "refusal": null,
                    "role": "assistant",
                    "tool_calls": [],
                    "parsed": null
                }
            }
        ],
        "created": 1733486708,
        "model": "gpt-4o-2024-08-06",
        "object": "chat.completion",
        "system_fingerprint": "fp_c7ca0ebaca",
        "usage": {
            "completion_tokens": 4,
            "prompt_tokens": 25,
            "total_tokens": 29,
            "completion_tokens_details": {
                "accepted_prediction_tokens": 0,
                "audio_tokens": 0,
                "reasoning_tokens": 0,
                "rejected_prediction_tokens": 0
            },
            "prompt_tokens_details": {
                "audio_tokens": 0,
                "cached_tokens": 0
            }
        }
    }"""
    return UploadFile(filename='test.json', file=BytesIO(json_content.encode()))


def get_incorrect_sample_json_file() -> UploadFile:
    json_content = """
    {
        "id": "chatcmpl-0120",
        "created": 1733486708,
        "model": "gpt-4o-2024-08-06",
        "object": "chat.completion",
        "system_fingerprint": "fp_c7ca0ebaca",
    }"""
    return UploadFile(filename='test.json', file=BytesIO(json_content.encode()))
