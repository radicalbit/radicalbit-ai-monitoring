test_drift_res = {
    "feature_metrics": [
        {
            "feature_name": "cat1",
            "drift_calc": {
                "type": "CHI2",
                "value": 0.0004993992273872871,
                "has_drift": True,
            },
        },
        {
            "feature_name": "cat2",
            "drift_calc": {
                "type": "CHI2",
                "value": 0.49015296041582523,
                "has_drift": False,
            },
        },
        {
            "feature_name": "num1",
            "drift_calc": {"type": "KS", "value": 0.9, "has_drift": True},
        },
        {
            "feature_name": "num2",
            "drift_calc": {"type": "KS", "value": 0.3, "has_drift": False},
        },
    ]
}

test_drift_small_res = {
    "feature_metrics": [
        {
            "feature_name": "cat1",
            "drift_calc": {"type": "CHI2", "value": None, "has_drift": False},
        },
        {
            "feature_name": "cat2",
            "drift_calc": {"type": "CHI2", "value": None, "has_drift": False},
        },
        {
            "feature_name": "num1",
            "drift_calc": {"type": "KS", "value": 0.75, "has_drift": False},
        },
        {
            "feature_name": "num2",
            "drift_calc": {"type": "KS", "value": 0.7, "has_drift": False},
        },
    ]
}

test_drift_boolean_res = {
    "feature_metrics": [
        {
            "feature_name": "cat1",
            "drift_calc": {
                "type": "CHI2",
                "value": 0.0012340980408668267,
                "has_drift": True,
            },
        },
        {
            "feature_name": "bool1",
            "drift_calc": {
                "type": "CHI2",
                "value": 0.002699796063260207,
                "has_drift": True,
            },
        },
        {
            "feature_name": "num1",
            "drift_calc": {"type": "KS", "value": 0.4, "has_drift": False},
        },
        {
            "feature_name": "num2",
            "drift_calc": {"type": "KS", "value": 0.3, "has_drift": False},
        },
    ]
}

test_drift_bigger_file_res = {
    "feature_metrics": [
        {
            "feature_name": "cat1",
            "drift_calc": {
                "type": "CHI2",
                "value": 0.26994857272252293,
                "has_drift": False,
            },
        },
        {
            "feature_name": "cat2",
            "drift_calc": {
                "type": "CHI2",
                "value": 0.3894236957350261,
                "has_drift": False,
            },
        },
        {
            "feature_name": "num1",
            "drift_calc": {
                "type": "KS",
                "value": 0.9230769231,
                "has_drift": True,
            },
        },
        {
            "feature_name": "num2",
            "drift_calc": {
                "type": "KS",
                "value": 0.5384615385,
                "has_drift": False,
            },
        },
    ]
}
