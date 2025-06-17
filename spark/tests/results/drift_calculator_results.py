test_drift_res = {
    'feature_metrics': [
        {
            'feature_name': 'cat1',
            'field_type': 'categorical',
            'drift_calc': [
                {'type': 'CHI2', 'value': 1.0, 'has_drift': False, 'limit': 0.05}
            ],
        },
        {
            'feature_name': 'cat2',
            'field_type': 'categorical',
            'drift_calc': [
                {
                    'type': 'CHI2',
                    'value': 2.5396285894708634e-10,
                    'has_drift': True,
                    'limit': 0.05,
                }
            ],
        },
        {
            'feature_name': 'num1',
            'field_type': 'numerical',
            'drift_calc': [
                {
                    'type': 'KS',
                    'value': 0.9,
                    'has_drift': True,
                    'limit': 0.6073614619083052,
                }
            ],
        },
        {
            'feature_name': 'num2',
            'field_type': 'numerical',
            'drift_calc': [
                {
                    'type': 'KS',
                    'value': 0.3,
                    'has_drift': False,
                    'limit': 0.6073614619083052,
                }
            ],
        },
    ]
}

test_drift_small_res = {
    'feature_metrics': [
        {
            'feature_name': 'cat1',
            'field_type': 'categorical',
            'drift_calc': [
                {
                    'type': 'CHI2',
                    'value': 0.7788007830714049,
                    'has_drift': False,
                    'limit': 0.05,
                }
            ],
        },
        {
            'feature_name': 'cat2',
            'field_type': 'categorical',
            'drift_calc': [
                {
                    'type': 'CHI2',
                    'value': 0.007660761135179449,
                    'has_drift': True,
                    'limit': 0.05,
                }
            ],
        },
        {
            'feature_name': 'num1',
            'field_type': 'numerical',
            'drift_calc': [
                {
                    'type': 'KS',
                    'value': 0.75,
                    'has_drift': False,
                    'limit': 0.8034636920670024,
                }
            ],
        },
        {
            'feature_name': 'num2',
            'field_type': 'numerical',
            'drift_calc': [
                {
                    'type': 'KS',
                    'value': 0.7,
                    'has_drift': False,
                    'limit': 0.8034636920670024,
                }
            ],
        },
    ]
}

test_drift_boolean_res = {
    'feature_metrics': [
        {
            'feature_name': 'cat1',
            'field_type': 'categorical',
            'drift_calc': [
                {'type': 'CHI2', 'value': 1.0, 'has_drift': False, 'limit': 0.05}
            ],
        },
        {
            'feature_name': 'bool1',
            'field_type': 'categorical',
            'drift_calc': [
                {'type': 'CHI2', 'value': 1.0, 'has_drift': False, 'limit': 0.05}
            ],
        },
        {
            'feature_name': 'num1',
            'field_type': 'numerical',
            'drift_calc': [
                {
                    'type': 'KS',
                    'value': 0.4,
                    'has_drift': False,
                    'limit': 0.6073614619083052,
                }
            ],
        },
        {
            'feature_name': 'num2',
            'field_type': 'numerical',
            'drift_calc': [
                {
                    'type': 'KS',
                    'value': 0.3,
                    'has_drift': False,
                    'limit': 0.6073614619083052,
                }
            ],
        },
    ]
}

test_drift_bigger_file_res = {
    'feature_metrics': [
        {
            'feature_name': 'cat1',
            'field_type': 'categorical',
            'drift_calc': [
                {
                    'type': 'CHI2',
                    'value': 0.7074036474040617,
                    'has_drift': False,
                    'limit': 0.05,
                }
            ],
        },
        {
            'feature_name': 'cat2',
            'field_type': 'categorical',
            'drift_calc': [
                {
                    'type': 'CHI2',
                    'value': 1.3668274623882378e-07,
                    'has_drift': True,
                    'limit': 0.05,
                }
            ],
        },
        {
            'feature_name': 'num1',
            'field_type': 'numerical',
            'drift_calc': [
                {
                    'type': 'KS',
                    'value': 0.9230769231,
                    'has_drift': True,
                    'limit': 0.5712477148401375,
                }
            ],
        },
        {
            'feature_name': 'num2',
            'field_type': 'numerical',
            'drift_calc': [
                {
                    'type': 'KS',
                    'value': 0.5384615385,
                    'has_drift': False,
                    'limit': 0.5712477148401375,
                }
            ],
        },
    ]
}

test_drift_bike_res = {
    'feature_metrics': [
        {
            'feature_name': 'season',
            'field_type': 'categorical',
            'drift_calc': [
                {
                    'type': 'CHI2',
                    'value': 1.5727996539817032e-36,
                    'has_drift': True,
                    'limit': 0.05,
                }
            ],
        },
        {
            'feature_name': 'yr',
            'field_type': 'categorical',
            'drift_calc': [
                {
                    'type': 'CHI2',
                    'value': 1.3270931223367946e-23,
                    'has_drift': True,
                    'limit': 0.05,
                }
            ],
        },
        {
            'feature_name': 'mnth',
            'field_type': 'categorical',
            'drift_calc': [
                {
                    'type': 'CHI2',
                    'value': 1.1116581506687278e-44,
                    'has_drift': True,
                    'limit': 0.05,
                }
            ],
        },
        {
            'feature_name': 'holiday',
            'field_type': 'categorical',
            'drift_calc': [
                {
                    'type': 'CHI2',
                    'value': 0.6115640463654775,
                    'has_drift': False,
                    'limit': 0.05,
                }
            ],
        },
        {
            'feature_name': 'weekday',
            'field_type': 'categorical',
            'drift_calc': [
                {
                    'type': 'CHI2',
                    'value': 0.9998169413361089,
                    'has_drift': False,
                    'limit': 0.05,
                }
            ],
        },
        {
            'feature_name': 'workingday',
            'field_type': 'categorical',
            'drift_calc': [
                {
                    'type': 'CHI2',
                    'value': 0.730645812540401,
                    'has_drift': False,
                    'limit': 0.05,
                }
            ],
        },
        {
            'feature_name': 'weathersit',
            'field_type': 'numerical',
            'drift_calc': [
                {
                    'type': 'KS',
                    'value': 0.6219091927,
                    'has_drift': True,
                    'limit': 0.14480183228052304,
                }
            ],
        },
        {
            'feature_name': 'temp',
            'field_type': 'numerical',
            'drift_calc': [
                {
                    'type': 'KS',
                    'value': 0.5259741552,
                    'has_drift': True,
                    'limit': 0.14480183228052304,
                }
            ],
        },
        {
            'feature_name': 'atemp',
            'field_type': 'numerical',
            'drift_calc': [
                {
                    'type': 'KS',
                    'value': 0.5322880465,
                    'has_drift': True,
                    'limit': 0.14480183228052304,
                }
            ],
        },
        {
            'feature_name': 'hum',
            'field_type': 'numerical',
            'drift_calc': [
                {
                    'type': 'KS',
                    'value': 0.2230727748,
                    'has_drift': True,
                    'limit': 0.14480183228052304,
                }
            ],
        },
        {
            'feature_name': 'windspeed',
            'field_type': 'numerical',
            'drift_calc': [
                {
                    'type': 'KS',
                    'value': 0.2180156245,
                    'has_drift': True,
                    'limit': 0.14480183228052304,
                }
            ],
        },
    ]
}

test_drift_phone_res = {
    'feature_metrics': [
        {
            'feature_name': 'brand_name',
            'field_type': 'categorical',
            'drift_calc': [
                {'type': 'CHI2', 'limit': 0.05, 'value': 1.0, 'has_drift': False}
            ],
        },
        {
            'feature_name': 'model',
            'field_type': 'categorical',
            'drift_calc': [
                {'type': 'JS', 'value': 0.0, 'has_drift': False, 'limit': 0.1}
            ],
        },
        {
            'feature_name': 'price',
            'field_type': 'numerical',
            'drift_calc': [
                {
                    'type': 'KS',
                    'limit': 0.06135277262096252,
                    'value': 0.0199795918,
                    'has_drift': False,
                }
            ],
        },
        {
            'feature_name': 'rating',
            'field_type': 'numerical',
            'drift_calc': [
                {'type': 'WASSERSTEIN', 'limit': 0.1, 'value': 400.0, 'has_drift': True}
            ],
        },
        {
            'feature_name': 'has_5g',
            'field_type': 'categorical',
            'drift_calc': [
                {
                    'type': 'KULLBACK',
                    'value': 0.00010331230697302376,
                    'has_drift': False,
                    'limit': 0.1,
                }
            ],
        },
        {
            'feature_name': 'has_nfc',
            'field_type': 'categorical',
            'drift_calc': [
                {
                    'type': 'HELLINGER',
                    'limit': 0.1,
                    'value': 0.001676393838803299,
                    'has_drift': False,
                }
            ],
        },
        {
            'feature_name': 'has_ir_blaster',
            'field_type': 'categorical',
            'drift_calc': [
                {'type': 'CHI2', 'limit': 0.05, 'value': 1.0, 'has_drift': False}
            ],
        },
        {
            'feature_name': 'processor_brand',
            'field_type': 'categorical',
            'drift_calc': [
                {
                    'type': 'JS',
                    'value': 0.7677812405779812,
                    'has_drift': True,
                    'limit': 0.1,
                }
            ],
        },
        {
            'feature_name': 'num_cores',
            'field_type': 'categorical',
            'drift_calc': [
                {
                    'type': 'KS',
                    'limit': 0.06135277262096252,
                    'value': 0.9219154519,
                    'has_drift': True,
                }
            ],
        },
        {
            'feature_name': 'processor_speed',
            'field_type': 'numerical',
            'drift_calc': [
                {'type': 'WASSERSTEIN', 'limit': 0.1, 'value': 0.0, 'has_drift': False}
            ],
        },
        {
            'feature_name': 'battery_capacity',
            'field_type': 'numerical',
            'drift_calc': [
                {'type': 'PSI', 'limit': 0.1, 'value': 0.0, 'has_drift': False}
            ],
        },
        {
            'feature_name': 'fast_charging_available',
            'field_type': 'categorical',
            'drift_calc': [
                {'type': 'CHI2', 'limit': 0.05, 'value': 1.0, 'has_drift': False}
            ],
        },
        {
            'feature_name': 'fast_charging',
            'field_type': 'numerical',
            'drift_calc': [
                {'type': 'JS', 'value': -1.0, 'has_drift': False, 'limit': 0.1}
            ],
        },
        {
            'feature_name': 'ram_capacity',
            'field_type': 'categorical',
            'drift_calc': [
                {'type': 'KULLBACK', 'value': 0.0, 'has_drift': False, 'limit': 0.1}
            ],
        },
        {
            'feature_name': 'internal_memory',
            'field_type': 'categorical',
            'drift_calc': [
                {
                    'type': 'JS',
                    'value': 0.0018992979350567496,
                    'has_drift': False,
                    'limit': 0.1,
                }
            ],
        },
        {
            'feature_name': 'screen_size',
            'field_type': 'numerical',
            'drift_calc': [
                {
                    'type': 'KS',
                    'limit': 0.06135277262096252,
                    'value': 0.119877551,
                    'has_drift': True,
                }
            ],
        },
        {
            'feature_name': 'refresh_rate',
            'field_type': 'numerical',
            'drift_calc': [
                {
                    'type': 'WASSERSTEIN',
                    'limit': 0.1,
                    'value': 0.24489795918367474,
                    'has_drift': True,
                }
            ],
        },
        {
            'feature_name': 'num_rear_cameras',
            'field_type': 'categorical',
            'drift_calc': [
                {'type': 'JS', 'value': 0.0, 'has_drift': False, 'limit': 0.1}
            ],
        },
        {
            'feature_name': 'num_front_cameras',
            'field_type': 'categorical',
            'drift_calc': [
                {'type': 'KULLBACK', 'value': 0.0, 'has_drift': False, 'limit': 0.1}
            ],
        },
        {
            'feature_name': 'os',
            'field_type': 'categorical',
            'drift_calc': [
                {
                    'type': 'HELLINGER',
                    'limit': 0.1,
                    'value': 0.00021263417278494462,
                    'has_drift': False,
                }
            ],
        },
        {
            'feature_name': 'primary_camera_rear',
            'field_type': 'numerical',
            'drift_calc': [
                {'type': 'WASSERSTEIN', 'limit': 0.1, 'value': 0.0, 'has_drift': False}
            ],
        },
        {
            'feature_name': 'primary_camera_front',
            'field_type': 'numerical',
            'drift_calc': [
                {'type': 'WASSERSTEIN', 'limit': 0.1, 'value': 0.0, 'has_drift': False}
            ],
        },
        {
            'feature_name': 'extended_memory_available',
            'field_type': 'categorical',
            'drift_calc': [
                {'type': 'JS', 'value': 0.0, 'has_drift': False, 'limit': 0.1}
            ],
        },
        {
            'feature_name': 'extended_upto',
            'field_type': 'categorical',
            'drift_calc': [
                {'type': 'KULLBACK', 'value': 0.0, 'has_drift': False, 'limit': 0.1}
            ],
        },
        {
            'feature_name': 'resolution_width',
            'field_type': 'categorical',
            'drift_calc': [
                {
                    'type': 'HELLINGER',
                    'limit': 0.1,
                    'value': 0.0012353117525546015,
                    'has_drift': False,
                }
            ],
        },
        {
            'feature_name': 'resolution_height',
            'field_type': 'categorical',
            'drift_calc': [
                {'type': 'CHI2', 'limit': 0.05, 'value': 1.0, 'has_drift': False}
            ],
        },
    ]
}

test_drift_demo_multiclass = {
    'feature_metrics': [
        {
            'feature_name': 'age',
            'field_type': 'numerical',
            'drift_calc': [
                {
                    'type': 'KS',
                    'limit': 0.08347829874882016,
                    'value': 0.0688229296,
                    'has_drift': False,
                },
                {
                    'type': 'WASSERSTEIN',
                    'limit': 0.1,
                    'value': 0.2976322646425741,
                    'has_drift': True,
                },
                {
                    'type': 'JS',
                    'value': 0.04238238499815362,
                    'has_drift': False,
                    'limit': 0.1,
                },
                {
                    'type': 'KULLBACK',
                    'value': 0.007115423962266981,
                    'has_drift': False,
                    'limit': 0.1,
                },
                {
                    'type': 'HELLINGER',
                    'limit': 0.1,
                    'value': 0.02571266024808534,
                    'has_drift': False,
                },
                {
                    'type': 'PSI',
                    'limit': 0.1,
                    'value': 0.007345059792257203,
                    'has_drift': False,
                },
            ],
        },
        {
            'feature_name': 'sex',
            'field_type': 'numerical',
            'drift_calc': [
                {
                    'type': 'KS',
                    'limit': 0.08347829874882016,
                    'value': 0.6678903696,
                    'has_drift': True,
                },
                {
                    'type': 'WASSERSTEIN',
                    'limit': 0.1,
                    'value': 0.02621502209131077,
                    'has_drift': False,
                },
                {'type': 'JS', 'value': -1.0, 'has_drift': False, 'limit': 0.1},
                {'type': 'KULLBACK', 'value': -1.0, 'has_drift': False, 'limit': 0.1},
                {
                    'type': 'HELLINGER',
                    'limit': 0.1,
                    'value': 0.10089933328314889,
                    'has_drift': True,
                },
                {
                    'type': 'PSI',
                    'limit': 0.1,
                    'value': 0.003046314772254488,
                    'has_drift': False,
                },
            ],
        },
        {
            'feature_name': 'cp',
            'field_type': 'numerical',
            'drift_calc': [
                {
                    'type': 'KS',
                    'limit': 0.08347829874882016,
                    'value': 0.4729695751,
                    'has_drift': True,
                },
                {
                    'type': 'WASSERSTEIN',
                    'limit': 0.1,
                    'value': 0.014557607341112472,
                    'has_drift': False,
                },
                {'type': 'JS', 'value': -1.0, 'has_drift': False, 'limit': 0.1},
                {'type': 'KULLBACK', 'value': -1.0, 'has_drift': False, 'limit': 0.1},
                {
                    'type': 'HELLINGER',
                    'limit': 0.1,
                    'value': 0.07881791799503131,
                    'has_drift': False,
                },
                {
                    'type': 'PSI',
                    'limit': 0.1,
                    'value': 0.002381855887031389,
                    'has_drift': False,
                },
            ],
        },
        {
            'feature_name': 'trestbps',
            'field_type': 'numerical',
            'drift_calc': [
                {
                    'type': 'KS',
                    'limit': 0.08347829874882016,
                    'value': 0.1478052373,
                    'has_drift': True,
                },
                {
                    'type': 'WASSERSTEIN',
                    'limit': 0.1,
                    'value': 1.0718987198368632,
                    'has_drift': True,
                },
                {'type': 'JS', 'value': -1.0, 'has_drift': False, 'limit': 0.1},
                {'type': 'KULLBACK', 'value': -1.0, 'has_drift': False, 'limit': 0.1},
                {
                    'type': 'HELLINGER',
                    'limit': 0.1,
                    'value': 0.06343339961431972,
                    'has_drift': False,
                },
                {
                    'type': 'PSI',
                    'limit': 0.1,
                    'value': 0.015882772365648907,
                    'has_drift': False,
                },
            ],
        },
        {
            'feature_name': 'chol',
            'field_type': 'numerical',
            'drift_calc': [
                {
                    'type': 'KS',
                    'limit': 0.08347829874882016,
                    'value': 0.0503397282,
                    'has_drift': False,
                },
                {
                    'type': 'WASSERSTEIN',
                    'limit': 0.1,
                    'value': 3.033006684037611,
                    'has_drift': True,
                },
                {
                    'type': 'JS',
                    'value': 0.03988705401267132,
                    'has_drift': False,
                    'limit': 0.1,
                },
                {
                    'type': 'KULLBACK',
                    'value': 0.006331911610811417,
                    'has_drift': False,
                    'limit': 0.1,
                },
                {
                    'type': 'HELLINGER',
                    'limit': 0.1,
                    'value': 0.04310417911349321,
                    'has_drift': False,
                },
                {
                    'type': 'PSI',
                    'limit': 0.1,
                    'value': 0.008114817224887624,
                    'has_drift': False,
                },
            ],
        },
        {
            'feature_name': 'fbs',
            'field_type': 'numerical',
            'drift_calc': [
                {
                    'type': 'KS',
                    'limit': 0.08347829874882016,
                    'value': 0.8533646766,
                    'has_drift': True,
                },
                {
                    'type': 'WASSERSTEIN',
                    'limit': 0.1,
                    'value': 0.0018182848079755232,
                    'has_drift': False,
                },
                {'type': 'JS', 'value': -1.0, 'has_drift': False, 'limit': 0.1},
                {'type': 'KULLBACK', 'value': -1.0, 'has_drift': False, 'limit': 0.1},
                {
                    'type': 'HELLINGER',
                    'limit': 0.1,
                    'value': 0.08264542675759168,
                    'has_drift': False,
                },
                {
                    'type': 'PSI',
                    'limit': 0.1,
                    'value': 0.00002643955913746645,
                    'has_drift': False,
                },
            ],
        },
        {
            'feature_name': 'restecg',
            'field_type': 'numerical',
            'drift_calc': [
                {
                    'type': 'KS',
                    'limit': 0.08347829874882016,
                    'value': 0.5044635777,
                    'has_drift': True,
                },
                {
                    'type': 'WASSERSTEIN',
                    'limit': 0.1,
                    'value': 0.008570295683697715,
                    'has_drift': False,
                },
                {'type': 'JS', 'value': -1.0, 'has_drift': False, 'limit': 0.1},
                {'type': 'KULLBACK', 'value': -1.0, 'has_drift': False, 'limit': 0.1},
                {
                    'type': 'HELLINGER',
                    'limit': 0.1,
                    'value': 0.07758713261378634,
                    'has_drift': False,
                },
                {
                    'type': 'PSI',
                    'limit': 0.1,
                    'value': 0.0002815053813634207,
                    'has_drift': False,
                },
            ],
        },
        {
            'feature_name': 'thalach',
            'field_type': 'numerical',
            'drift_calc': [
                {
                    'type': 'KS',
                    'limit': 0.08347829874882016,
                    'value': 0.0446838552,
                    'has_drift': False,
                },
                {
                    'type': 'WASSERSTEIN',
                    'limit': 0.1,
                    'value': 1.1437521241644952,
                    'has_drift': True,
                },
                {
                    'type': 'JS',
                    'value': 0.05363859859339404,
                    'has_drift': False,
                    'limit': 0.1,
                },
                {
                    'type': 'KULLBACK',
                    'value': 0.011505666152398456,
                    'has_drift': False,
                    'limit': 0.1,
                },
                {
                    'type': 'HELLINGER',
                    'limit': 0.1,
                    'value': 0.06310419947459686,
                    'has_drift': False,
                },
                {
                    'type': 'PSI',
                    'limit': 0.1,
                    'value': 0.025866680531071856,
                    'has_drift': False,
                },
            ],
        },
        {
            'feature_name': 'exang',
            'field_type': 'numerical',
            'drift_calc': [
                {
                    'type': 'KS',
                    'limit': 0.08347829874882016,
                    'value': 0.6830350062,
                    'has_drift': True,
                },
                {
                    'type': 'WASSERSTEIN',
                    'limit': 0.1,
                    'value': 0.006746346437068063,
                    'has_drift': False,
                },
                {'type': 'JS', 'value': -1.0, 'has_drift': False, 'limit': 0.1},
                {'type': 'KULLBACK', 'value': -1.0, 'has_drift': False, 'limit': 0.1},
                {
                    'type': 'HELLINGER',
                    'limit': 0.1,
                    'value': 0.08631734638438168,
                    'has_drift': False,
                },
                {
                    'type': 'PSI',
                    'limit': 0.1,
                    'value': 0.00020940618968498672,
                    'has_drift': False,
                },
            ],
        },
        {
            'feature_name': 'oldpeak',
            'field_type': 'numerical',
            'drift_calc': [
                {
                    'type': 'KS',
                    'limit': 0.08347829874882016,
                    'value': 0.3322288599,
                    'has_drift': True,
                },
                {
                    'type': 'WASSERSTEIN',
                    'limit': 0.1,
                    'value': 0.046041690268494424,
                    'has_drift': False,
                },
                {'type': 'JS', 'value': -1.0, 'has_drift': False, 'limit': 0.1},
                {'type': 'KULLBACK', 'value': -1.0, 'has_drift': False, 'limit': 0.1},
                {
                    'type': 'HELLINGER',
                    'limit': 0.1,
                    'value': 0.05380878566325148,
                    'has_drift': False,
                },
                {
                    'type': 'PSI',
                    'limit': 0.1,
                    'value': 0.033555282741715695,
                    'has_drift': False,
                },
            ],
        },
        {
            'feature_name': 'slope',
            'field_type': 'numerical',
            'drift_calc': [
                {
                    'type': 'KS',
                    'limit': 0.08347829874882016,
                    'value': 0.4784194558,
                    'has_drift': True,
                },
                {
                    'type': 'WASSERSTEIN',
                    'limit': 0.1,
                    'value': 0.009992069785884183,
                    'has_drift': False,
                },
                {'type': 'JS', 'value': -1.0, 'has_drift': False, 'limit': 0.1},
                {'type': 'KULLBACK', 'value': -1.0, 'has_drift': False, 'limit': 0.1},
                {
                    'type': 'HELLINGER',
                    'limit': 0.1,
                    'value': 0.08313730034383332,
                    'has_drift': False,
                },
                {
                    'type': 'PSI',
                    'limit': 0.1,
                    'value': 0.001131194032448127,
                    'has_drift': False,
                },
            ],
        },
        {
            'feature_name': 'ca',
            'field_type': 'numerical',
            'drift_calc': [
                {
                    'type': 'KS',
                    'limit': 0.08347829874882016,
                    'value': 0.6143536875,
                    'has_drift': True,
                },
                {
                    'type': 'WASSERSTEIN',
                    'limit': 0.1,
                    'value': 0.016553465691396707,
                    'has_drift': False,
                },
                {'type': 'JS', 'value': -1.0, 'has_drift': False, 'limit': 0.1},
                {'type': 'KULLBACK', 'value': -1.0, 'has_drift': False, 'limit': 0.1},
                {
                    'type': 'HELLINGER',
                    'limit': 0.1,
                    'value': 0.07284632051190043,
                    'has_drift': False,
                },
                {
                    'type': 'PSI',
                    'limit': 0.1,
                    'value': 0.0010672486757116548,
                    'has_drift': False,
                },
            ],
        },
        {
            'feature_name': 'thal',
            'field_type': 'numerical',
            'drift_calc': [
                {
                    'type': 'KS',
                    'limit': 0.08347829874882016,
                    'value': 0.5586809595,
                    'has_drift': True,
                },
                {
                    'type': 'WASSERSTEIN',
                    'limit': 0.1,
                    'value': 0.029453412630982667,
                    'has_drift': False,
                },
                {'type': 'JS', 'value': -1.0, 'has_drift': False, 'limit': 0.1},
                {'type': 'KULLBACK', 'value': -1.0, 'has_drift': False, 'limit': 0.1},
                {
                    'type': 'HELLINGER',
                    'limit': 0.1,
                    'value': 0.07275281561783288,
                    'has_drift': False,
                },
                {
                    'type': 'PSI',
                    'limit': 0.1,
                    'value': 0.0036391571010142725,
                    'has_drift': False,
                },
            ],
        },
    ]
}
