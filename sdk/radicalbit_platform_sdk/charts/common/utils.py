from typing import List


def get_formatted_bucket_data(bucket_data: List[str]) -> List[str]:
    bucket_data_formatted = []
    bucket_data_len = len(bucket_data) - 1

    for idx, d in enumerate(bucket_data):
        close_bracket = ']' if idx == bucket_data_len - 1 else ')'
        if idx < bucket_data_len:
            element = '[' + str(d) + ',' + str(bucket_data[idx + 1]) + close_bracket
            bucket_data_formatted.append(element)

    return bucket_data_formatted


def get_chart_header(title: str):
    return {
        'title': {'text': title, 'textStyle': {'fontSize': 14}},
        'legend': {'center': 'center'},
    }
