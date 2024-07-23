test_drift_res = {
    "feature_metrics": [
        {
            "feature_name": "cat1",
            "drift_calc": {"type": "CHI2", "value": 1.0, "has_drift": False},
        },
        {
            "feature_name": "cat2",
            "drift_calc": {
                "type": "CHI2",
                "value": 3.4671076872696563e-05,
                "has_drift": True,
            },
        },
        {
            "feature_name": "num1",
            "drift_calc": {"type": "CHI2", "value": 0.0, "has_drift": True},
        },
        {
            "feature_name": "num2",
            "drift_calc": {"type": "CHI2", "value": 1.0, "has_drift": False},
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
            "drift_calc": {"type": "CHI2", "value": None, "has_drift": False},
        },
        {
            "feature_name": "num2",
            "drift_calc": {"type": "CHI2", "value": None, "has_drift": False},
        },
    ]
}

test_drift_boolean_res = {
    "feature_metrics": [
        {
            "feature_name": "cat1",
            "drift_calc": {"type": "CHI2", "value": 1.0, "has_drift": False},
        },
        {
            "feature_name": "bool1",
            "drift_calc": {"type": "CHI2", "value": 1.0, "has_drift": False},
        },
        {
            "feature_name": "num1",
            "drift_calc": {"type": "CHI2", "value": 1.0, "has_drift": False},
        },
        {
            "feature_name": "num2",
            "drift_calc": {"type": "CHI2", "value": 1.0, "has_drift": False},
        },
    ]
}

test_drift_bigger_file_res = {
    "feature_metrics": [
        {
            "feature_name": "cat1",
            "drift_calc": {"type": "CHI2", "value": 0.0, "has_drift": True},
        },
        {
            "feature_name": "cat2",
            "drift_calc": {
                "type": "CHI2",
                "value": 0.052807511416113395,
                "has_drift": False,
            },
        },
        {
            "feature_name": "num1",
            "drift_calc": {"type": "CHI2", "value": 0.0, "has_drift": True},
        },
        {
            "feature_name": "num2",
            "drift_calc": {"type": "CHI2", "value": 0.0, "has_drift": True},
        },
    ]
}

test_drift_bike_res = {
    "feature_metrics": [
        {
            "feature_name": "weathersit",
            "drift_calc": {
                "type": "CHI2",
                "value": 0.002631773674724352,
                "has_drift": True,
            },
        },
        {
            "feature_name": "temp",
            "drift_calc": {"type": "KS", "value": 0.5259741552, "has_drift": True},
        },
        {
            "feature_name": "atemp",
            "drift_calc": {"type": "KS", "value": 0.5322880465, "has_drift": True},
        },
        {
            "feature_name": "hum",
            "drift_calc": {"type": "KS", "value": 0.2230727748, "has_drift": True},
        },
        {
            "feature_name": "windspeed",
            "drift_calc": {"type": "KS", "value": 0.2180156245, "has_drift": True},
        },
        {
            "feature_name": "season",
            "drift_calc": {"type": "CHI2", "value": 0.0, "has_drift": True},
        },
        {
            "feature_name": "yr",
            "drift_calc": {"type": "CHI2", "value": 0.0, "has_drift": True},
        },
        {
            "feature_name": "mnth",
            "drift_calc": {"type": "CHI2", "value": 0.0, "has_drift": True},
        },
        {
            "feature_name": "holiday",
            "drift_calc": {"type": "CHI2", "value": 1.0, "has_drift": False},
        },
        {
            "feature_name": "weekday",
            "drift_calc": {
                "type": "CHI2",
                "value": 0.7855334068007708,
                "has_drift": False,
            },
        },
        {
            "feature_name": "workingday",
            "drift_calc": {
                "type": "CHI2",
                "value": 0.6625205835400574,
                "has_drift": False,
            },
        },
    ]
}

test_drift_phone_res = {
    "feature_metrics": [
        {
            "feature_name": "brand_name",
            "drift_calc": {"type": "CHI2", "value": 1.0, "has_drift": False},
        },
        {
            "feature_name": "model",
            "drift_calc": {"type": "CHI2", "value": 1.0, "has_drift": False},
        },
        {
            "feature_name": "has_5g",
            "drift_calc": {
                "type": "CHI2",
                "value": 0.6528883189652503,
                "has_drift": False,
            },
        },
        {
            "feature_name": "has_nfc",
            "drift_calc": {"type": "CHI2", "value": 1.0, "has_drift": False},
        },
        {
            "feature_name": "has_ir_blaster",
            "drift_calc": {"type": "CHI2", "value": 1.0, "has_drift": False},
        },
        {
            "feature_name": "processor_brand",
            "drift_calc": {"type": "CHI2", "value": 0.0, "has_drift": True},
        },
        {
            "feature_name": "os",
            "drift_calc": {"type": "CHI2", "value": 1.0, "has_drift": False},
        },
        {
            "feature_name": "rating",
            "drift_calc": {"type": "KS", "value": 0.9989795918, "has_drift": True},
        },
        {
            "feature_name": "processor_speed",
            "drift_calc": {"type": "KS", "value": 0.1541282799, "has_drift": True},
        },
        {
            "feature_name": "fast_charging",
            "drift_calc": {"type": "KS", "value": 0.196941691, "has_drift": True},
        },
        {
            "feature_name": "screen_size",
            "drift_calc": {"type": "KS", "value": 0.119877551, "has_drift": True},
        },
        {
            "feature_name": "primary_camera_rear",
            "drift_calc": {"type": "KS", "value": 0.3382259475, "has_drift": True},
        },
        {
            "feature_name": "primary_camera_front",
            "drift_calc": {"type": "KS", "value": 0.3139650146, "has_drift": True},
        },
        {
            "feature_name": "extended_upto",
            "drift_calc": {"type": "CHI2", "value": 1.0, "has_drift": False},
        },
        {
            "feature_name": "price",
            "drift_calc": {"type": "PSI", "value": 0.0, "has_drift": False},
        },
        {
            "feature_name": "num_cores",
            "drift_calc": {"type": "CHI2", "value": 1.0, "has_drift": False},
        },
        {
            "feature_name": "battery_capacity",
            "drift_calc": {"type": "PSI", "value": 0.0, "has_drift": False},
        },
        {
            "feature_name": "fast_charging_available",
            "drift_calc": {"type": "CHI2", "value": 1.0, "has_drift": False},
        },
        {
            "feature_name": "ram_capacity",
            "drift_calc": {"type": "CHI2", "value": 1.0, "has_drift": False},
        },
        {
            "feature_name": "internal_memory",
            "drift_calc": {
                "type": "CHI2",
                "value": 0.9999999717288575,
                "has_drift": False,
            },
        },
        {
            "feature_name": "refresh_rate",
            "drift_calc": {
                "type": "CHI2",
                "value": 0.9997655785111437,
                "has_drift": False,
            },
        },
        {
            "feature_name": "num_rear_cameras",
            "drift_calc": {"type": "CHI2", "value": 1.0, "has_drift": False},
        },
        {
            "feature_name": "num_front_cameras",
            "drift_calc": {"type": "CHI2", "value": 1.0, "has_drift": False},
        },
        {
            "feature_name": "extended_memory_available",
            "drift_calc": {"type": "CHI2", "value": 1.0, "has_drift": False},
        },
        {
            "feature_name": "resolution_width",
            "drift_calc": {"type": "PSI", "value": 0.0, "has_drift": False},
        },
        {
            "feature_name": "resolution_height",
            "drift_calc": {"type": "PSI", "value": 0.0, "has_drift": False},
        },
    ]
}
