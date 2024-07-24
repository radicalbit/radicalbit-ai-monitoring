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
                "value": 2.5396285894708634e-10,
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
            "drift_calc": {
                "type": "CHI2",
                "value": 0.7788007830714049,
                "has_drift": False,
            },
        },
        {
            "feature_name": "cat2",
            "drift_calc": {
                "type": "CHI2",
                "value": 0.007660761135179449,
                "has_drift": True,
            },
        },
        {
            "feature_name": "num1",
            "drift_calc": {"type": "CHI2", "value": 0.0, "has_drift": True},
        },
        {
            "feature_name": "num2",
            "drift_calc": {
                "type": "CHI2",
                "value": 0.4158801869955079,
                "has_drift": False,
            },
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
            "drift_calc": {
                "type": "CHI2",
                "value": 0.7074036474040617,
                "has_drift": False,
            },
        },
        {
            "feature_name": "cat2",
            "drift_calc": {
                "type": "CHI2",
                "value": 1.3668274623882378e-07,
                "has_drift": True,
            },
        },
        {
            "feature_name": "num1",
            "drift_calc": {"type": "CHI2", "value": 0.0, "has_drift": True},
        },
        {
            "feature_name": "num2",
            "drift_calc": {
                "type": "CHI2",
                "value": 0.9282493523958153,
                "has_drift": False,
            },
        },
    ]
}

test_drift_bike_res = {
    "feature_metrics": [
        {
            "feature_name": "weathersit",
            "drift_calc": {
                "type": "CHI2",
                "value": 0.5328493415823949,
                "has_drift": False,
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
            "drift_calc": {
                "type": "CHI2",
                "value": 1.5727996539817032e-36,
                "has_drift": True,
            },
        },
        {
            "feature_name": "yr",
            "drift_calc": {
                "type": "CHI2",
                "value": 1.3270931223367946e-23,
                "has_drift": True,
            },
        },
        {
            "feature_name": "mnth",
            "drift_calc": {
                "type": "CHI2",
                "value": 1.1116581506687278e-44,
                "has_drift": True,
            },
        },
        {
            "feature_name": "holiday",
            "drift_calc": {
                "type": "CHI2",
                "value": 0.6115640463654775,
                "has_drift": False,
            },
        },
        {
            "feature_name": "weekday",
            "drift_calc": {
                "type": "CHI2",
                "value": 0.9998169413361089,
                "has_drift": False,
            },
        },
        {
            "feature_name": "workingday",
            "drift_calc": {
                "type": "CHI2",
                "value": 0.730645812540401,
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
                "value": 0.652356328876868,
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
                "value": 0.9999999710826085,
                "has_drift": False,
            },
        },
        {
            "feature_name": "refresh_rate",
            "drift_calc": {
                "type": "CHI2",
                "value": 0.9997690818736329,
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
