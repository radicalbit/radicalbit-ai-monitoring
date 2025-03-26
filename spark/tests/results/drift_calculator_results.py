test_drift_res = {
    "feature_metrics": [
        {
            "feature_name": "cat1",
            "field_type": "categorical",
            "drift_calc": [
                {"type": "CHI2", "value": 1.0, "has_drift": False, "limit": 0.05}
            ],
        },
        {
            "feature_name": "cat2",
            "field_type": "categorical",
            "drift_calc": [
                {
                    "type": "CHI2",
                    "value": 2.5396285894708634e-10,
                    "has_drift": True,
                    "limit": 0.05,
                }
            ],
        },
        {
            "feature_name": "num1",
            "field_type": "numerical",
            "drift_calc": [
                {
                    "type": "KS",
                    "value": 0.9,
                    "has_drift": True,
                    "limit": 0.6073614619083052,
                }
            ],
        },
        {
            "feature_name": "num2",
            "field_type": "numerical",
            "drift_calc": [
                {
                    "type": "KS",
                    "value": 0.3,
                    "has_drift": False,
                    "limit": 0.6073614619083052,
                }
            ],
        },
    ]
}

test_drift_small_res = {
    "feature_metrics": [
        {
            "feature_name": "cat1",
            "field_type": "categorical",
            "drift_calc": [
                {
                    "type": "CHI2",
                    "value": 0.7788007830714049,
                    "has_drift": False,
                    "limit": 0.05,
                }
            ],
        },
        {
            "feature_name": "cat2",
            "field_type": "categorical",
            "drift_calc": [
                {
                    "type": "CHI2",
                    "value": 0.007660761135179449,
                    "has_drift": True,
                    "limit": 0.05,
                }
            ],
        },
        {
            "feature_name": "num1",
            "field_type": "numerical",
            "drift_calc": [
                {
                    "type": "KS",
                    "value": 0.75,
                    "has_drift": False,
                    "limit": 0.8034636920670024,
                }
            ],
        },
        {
            "feature_name": "num2",
            "field_type": "numerical",
            "drift_calc": [
                {
                    "type": "KS",
                    "value": 0.7,
                    "has_drift": False,
                    "limit": 0.8034636920670024,
                }
            ],
        },
    ]
}

test_drift_boolean_res = {
    "feature_metrics": [
        {
            "feature_name": "cat1",
            "field_type": "categorical",
            "drift_calc": [
                {"type": "CHI2", "value": 1.0, "has_drift": False, "limit": 0.05}
            ],
        },
        {
            "feature_name": "bool1",
            "field_type": "categorical",
            "drift_calc": [
                {"type": "CHI2", "value": 1.0, "has_drift": False, "limit": 0.05}
            ],
        },
        {
            "feature_name": "num1",
            "field_type": "numerical",
            "drift_calc": [
                {
                    "type": "KS",
                    "value": 0.4,
                    "has_drift": False,
                    "limit": 0.6073614619083052,
                }
            ],
        },
        {
            "feature_name": "num2",
            "field_type": "numerical",
            "drift_calc": [
                {
                    "type": "KS",
                    "value": 0.3,
                    "has_drift": False,
                    "limit": 0.6073614619083052,
                }
            ],
        },
    ]
}

test_drift_bigger_file_res = {
    "feature_metrics": [
        {
            "feature_name": "cat1",
            "field_type": "categorical",
            "drift_calc": [
                {
                    "type": "CHI2",
                    "value": 0.7074036474040617,
                    "has_drift": False,
                    "limit": 0.05,
                }
            ],
        },
        {
            "feature_name": "cat2",
            "field_type": "categorical",
            "drift_calc": [
                {
                    "type": "CHI2",
                    "value": 1.3668274623882378e-07,
                    "has_drift": True,
                    "limit": 0.05,
                }
            ],
        },
        {
            "feature_name": "num1",
            "field_type": "numerical",
            "drift_calc": [
                {
                    "type": "KS",
                    "value": 0.9230769231,
                    "has_drift": True,
                    "limit": 0.5712477148401375,
                }
            ],
        },
        {
            "feature_name": "num2",
            "field_type": "numerical",
            "drift_calc": [
                {
                    "type": "KS",
                    "value": 0.5384615385,
                    "has_drift": False,
                    "limit": 0.5712477148401375,
                }
            ],
        },
    ]
}

test_drift_bike_res = {
    "feature_metrics": [
        {
            "feature_name": "season",
            "field_type": "categorical",
            "drift_calc": [
                {
                    "type": "CHI2",
                    "value": 1.5727996539817032e-36,
                    "has_drift": True,
                    "limit": 0.05,
                }
            ],
        },
        {
            "feature_name": "yr",
            "field_type": "categorical",
            "drift_calc": [
                {
                    "type": "CHI2",
                    "value": 1.3270931223367946e-23,
                    "has_drift": True,
                    "limit": 0.05,
                }
            ],
        },
        {
            "feature_name": "mnth",
            "field_type": "categorical",
            "drift_calc": [
                {
                    "type": "CHI2",
                    "value": 1.1116581506687278e-44,
                    "has_drift": True,
                    "limit": 0.05,
                }
            ],
        },
        {
            "feature_name": "holiday",
            "field_type": "categorical",
            "drift_calc": [
                {
                    "type": "CHI2",
                    "value": 0.6115640463654775,
                    "has_drift": False,
                    "limit": 0.05,
                }
            ],
        },
        {
            "feature_name": "weekday",
            "field_type": "categorical",
            "drift_calc": [
                {
                    "type": "CHI2",
                    "value": 0.9998169413361089,
                    "has_drift": False,
                    "limit": 0.05,
                }
            ],
        },
        {
            "feature_name": "workingday",
            "field_type": "categorical",
            "drift_calc": [
                {
                    "type": "CHI2",
                    "value": 0.730645812540401,
                    "has_drift": False,
                    "limit": 0.05,
                }
            ],
        },
        {
            "feature_name": "weathersit",
            "field_type": "numerical",
            "drift_calc": [
                {
                    "type": "KS",
                    "value": 0.6219091927,
                    "has_drift": True,
                    "limit": 0.14480183228052304,
                }
            ],
        },
        {
            "feature_name": "temp",
            "field_type": "numerical",
            "drift_calc": [
                {
                    "type": "KS",
                    "value": 0.5259741552,
                    "has_drift": True,
                    "limit": 0.14480183228052304,
                }
            ],
        },
        {
            "feature_name": "atemp",
            "field_type": "numerical",
            "drift_calc": [
                {
                    "type": "KS",
                    "value": 0.5322880465,
                    "has_drift": True,
                    "limit": 0.14480183228052304,
                }
            ],
        },
        {
            "feature_name": "hum",
            "field_type": "numerical",
            "drift_calc": [
                {
                    "type": "KS",
                    "value": 0.2230727748,
                    "has_drift": True,
                    "limit": 0.14480183228052304,
                }
            ],
        },
        {
            "feature_name": "windspeed",
            "field_type": "numerical",
            "drift_calc": [
                {
                    "type": "KS",
                    "value": 0.2180156245,
                    "has_drift": True,
                    "limit": 0.14480183228052304,
                }
            ],
        },
    ]
}

test_drift_phone_res = {
    "feature_metrics": [
        {
            "feature_name": "brand_name",
            "field_type": "categorical",
            "drift_calc": [
                {"type": "CHI2", "value": 1.0, "has_drift": False, "limit": 0.05}
            ],
        },
        {
            "feature_name": "model",
            "field_type": "categorical",
            "drift_calc": [
                {"type": "CHI2", "value": 1.0, "has_drift": False, "limit": 0.05}
            ],
        },
        {
            "feature_name": "has_5g",
            "field_type": "categorical",
            "drift_calc": [
                {
                    "type": "CHI2",
                    "value": 0.652356328876868,
                    "has_drift": False,
                    "limit": 0.05,
                }
            ],
        },
        {
            "feature_name": "has_nfc",
            "field_type": "categorical",
            "drift_calc": [
                {"type": "CHI2", "value": 1.0, "has_drift": False, "limit": 0.05}
            ],
        },
        {
            "feature_name": "has_ir_blaster",
            "field_type": "categorical",
            "drift_calc": [
                {"type": "CHI2", "value": 1.0, "has_drift": False, "limit": 0.05}
            ],
        },
        {
            "feature_name": "processor_brand",
            "field_type": "categorical",
            "drift_calc": [
                {"type": "CHI2", "value": 0.0, "has_drift": True, "limit": 0.05}
            ],
        },
        {
            "feature_name": "num_cores",
            "field_type": "categorical",
            "drift_calc": [
                {"type": "CHI2", "value": 1.0, "has_drift": False, "limit": 0.05}
            ],
        },
        {
            "feature_name": "fast_charging_available",
            "field_type": "categorical",
            "drift_calc": [
                {"type": "CHI2", "value": 1.0, "has_drift": False, "limit": 0.05}
            ],
        },
        {
            "feature_name": "ram_capacity",
            "field_type": "categorical",
            "drift_calc": [
                {"type": "CHI2", "value": 1.0, "has_drift": False, "limit": 0.05}
            ],
        },
        {
            "feature_name": "internal_memory",
            "field_type": "categorical",
            "drift_calc": [
                {
                    "type": "CHI2",
                    "value": 0.9999999710826085,
                    "has_drift": False,
                    "limit": 0.05,
                }
            ],
        },
        {
            "feature_name": "num_rear_cameras",
            "field_type": "categorical",
            "drift_calc": [
                {"type": "CHI2", "value": 1.0, "has_drift": False, "limit": 0.05}
            ],
        },
        {
            "feature_name": "num_front_cameras",
            "field_type": "categorical",
            "drift_calc": [
                {"type": "CHI2", "value": 1.0, "has_drift": False, "limit": 0.05}
            ],
        },
        {
            "feature_name": "os",
            "field_type": "categorical",
            "drift_calc": [
                {"type": "CHI2", "value": 1.0, "has_drift": False, "limit": 0.05}
            ],
        },
        {
            "feature_name": "extended_memory_available",
            "field_type": "categorical",
            "drift_calc": [
                {"type": "CHI2", "value": 1.0, "has_drift": False, "limit": 0.05}
            ],
        },
        {
            "feature_name": "extended_upto",
            "field_type": "categorical",
            "drift_calc": [
                {"type": "CHI2", "value": 1.0, "has_drift": False, "limit": 0.05}
            ],
        },
        {
            "feature_name": "resolution_width",
            "field_type": "categorical",
            "drift_calc": [
                {"type": "CHI2", "value": 1.0, "has_drift": False, "limit": 0.05}
            ],
        },
        {
            "feature_name": "resolution_height",
            "field_type": "categorical",
            "drift_calc": [
                {"type": "CHI2", "value": 1.0, "has_drift": False, "limit": 0.05}
            ],
        },
        {
            "feature_name": "rating",
            "field_type": "numerical",
            "drift_calc": [
                {
                    "type": "KS",
                    "value": 0.9989795918,
                    "has_drift": True,
                    "limit": 0.06135277262096252,
                }
            ],
        },
        {
            "feature_name": "processor_speed",
            "field_type": "numerical",
            "drift_calc": [
                {
                    "type": "KS",
                    "value": 0.1541282799,
                    "has_drift": True,
                    "limit": 0.06135277262096252,
                }
            ],
        },
        {
            "feature_name": "fast_charging",
            "field_type": "numerical",
            "drift_calc": [
                {
                    "type": "KS",
                    "value": 0.196941691,
                    "has_drift": True,
                    "limit": 0.06135277262096252,
                }
            ],
        },
        {
            "feature_name": "screen_size",
            "field_type": "numerical",
            "drift_calc": [
                {
                    "type": "KS",
                    "value": 0.119877551,
                    "has_drift": True,
                    "limit": 0.06135277262096252,
                }
            ],
        },
        {
            "feature_name": "primary_camera_rear",
            "field_type": "numerical",
            "drift_calc": [
                {
                    "type": "KS",
                    "value": 0.3382259475,
                    "has_drift": True,
                    "limit": 0.06135277262096252,
                }
            ],
        },
        {
            "feature_name": "primary_camera_front",
            "field_type": "numerical",
            "drift_calc": [
                {
                    "type": "KS",
                    "value": 0.3139650146,
                    "has_drift": True,
                    "limit": 0.06135277262096252,
                }
            ],
        },
        {
            "feature_name": "price",
            "field_type": "numerical",
            "drift_calc": [
                {"type": "PSI", "value": 0.0, "has_drift": False, "limit": 0.1}
            ],
        },
        {
            "feature_name": "battery_capacity",
            "field_type": "numerical",
            "drift_calc": [
                {"type": "PSI", "value": 0.0, "has_drift": False, "limit": 0.1}
            ],
        },
        {
            "feature_name": "refresh_rate",
            "field_type": "numerical",
            "drift_calc": [
                {
                    "type": "PSI",
                    "value": 0.00011810925171709961,
                    "has_drift": False,
                    "limit": 0.1,
                }
            ],
        },
    ]
}
