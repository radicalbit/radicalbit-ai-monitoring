from utils.models import Granularity

# rbit_prefix = "rbit_spark"


def split_dict(dictionary):
    cleaned_dict = {}
    for k, v in dictionary.items():
        feature, metric = tuple(k.rsplit('-', 1))
        cleaned_dict.setdefault(feature, {})[metric] = v
    return cleaned_dict


def create_time_format(granularity: Granularity):
    match granularity:
        case Granularity.HOUR:
            return 'yyyy-MM-dd HH'
        case Granularity.DAY:
            return 'yyyy-MM-dd'
        case Granularity.WEEK:
            return 'yyyy-MM-dd'
        case Granularity.MONTH:
            return 'yyyy-MM'
