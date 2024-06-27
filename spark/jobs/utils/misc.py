def split_dict(dictionary):
    cleaned_dict = dict()
    for k, v in dictionary.items():
        feature, metric = tuple(k.rsplit("-", 1))
        cleaned_dict.setdefault(feature, dict())[metric] = v
    return cleaned_dict
