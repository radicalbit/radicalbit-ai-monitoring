test_calculation_dataset_target_int_stats_res = {
    'categorical': 2,
    'datetime': 1,
    'duplicate_rows': 0,
    'duplicate_rows_perc': 0.0,
    'missing_cells': 3,
    'missing_cells_perc': 4.285714285714286,
    'n_observations': 10,
    'n_variables': 7,
    'numeric': 4,
}

test_calculation_dataset_target_int_dq_res = {
    'n_observations': 10,
    'class_metrics': [
        {'name': '0', 'count': 3, 'percentage': 30.0},
        {'name': '1', 'count': 3, 'percentage': 30.0},
        {'name': '2', 'count': 3, 'percentage': 30.0},
        {'name': '3', 'count': 1, 'percentage': 10.0},
    ],
    'class_metrics_prediction': [
        {'name': '0', 'count': 2, 'percentage': 20.0},
        {'name': '1', 'count': 4, 'percentage': 40.0},
        {'name': '2', 'count': 2, 'percentage': 20.0},
        {'name': '3', 'count': 2, 'percentage': 20.0},
    ],
    'feature_metrics': [
        {
            'feature_name': 'num1',
            'type': 'numerical',
            'missing_value': {'count': 1, 'percentage': 10.0},
            'mean': 1.1666666666666667,
            'std': 0.75,
            'min': 0.5,
            'max': 3.0,
            'median_metrics': {'perc_25': 1.0, 'median': 1.0, 'perc_75': 1.0},
            'class_median_metrics': [],
            'histogram': {
                'buckets': [
                    0.5,
                    0.75,
                    1.0,
                    1.25,
                    1.5,
                    1.75,
                    2.0,
                    2.25,
                    2.5,
                    2.75,
                    3.0,
                ],
                'reference_values': [2, 0, 5, 0, 1, 0, 0, 0, 0, 1],
            },
        },
        {
            'feature_name': 'num2',
            'type': 'numerical',
            'missing_value': {'count': 2, 'percentage': 20.0},
            'mean': 277.675,
            'std': 201.88635947695215,
            'min': 1.4,
            'max': 499.0,
            'median_metrics': {
                'perc_25': 117.25,
                'median': 250.0,
                'perc_75': 499.0,
            },
            'class_median_metrics': [],
            'histogram': {
                'buckets': [
                    1.4,
                    51.160000000000004,
                    100.92000000000002,
                    150.68000000000004,
                    200.44000000000003,
                    250.20000000000002,
                    299.96000000000004,
                    349.72,
                    399.48,
                    449.24,
                    499.0,
                ],
                'reference_values': [1, 1, 1, 1, 0, 0, 1, 0, 0, 3],
            },
        },
        {
            'feature_name': 'cat1',
            'type': 'categorical',
            'missing_value': {'count': 0, 'percentage': 0.0},
            'category_frequency': [
                {'name': 'B', 'count': 4, 'frequency': 0.4},
                {'name': 'C', 'count': 1, 'frequency': 0.1},
                {'name': 'A', 'count': 5, 'frequency': 0.5},
            ],
            'distinct_value': 3,
        },
        {
            'feature_name': 'cat2',
            'type': 'categorical',
            'missing_value': {'count': 0, 'percentage': 0.0},
            'category_frequency': [
                {'name': 'Y', 'count': 1, 'frequency': 0.1},
                {'name': 'X', 'count': 9, 'frequency': 0.9},
            ],
            'distinct_value': 2,
        },
    ],
}

test_calculation_dataset_target_int_mq_res = {
    'classes': ['0', '1', '2', '3'],
    'class_metrics': [
        {
            'class_name': '0',
            'metrics': {
                'true_positive_rate': 0.6666666666666666,
                'false_positive_rate': 0.0,
                'precision': 1.0,
                'recall': 0.6666666666666666,
                'f_measure': 0.8,
            },
        },
        {
            'class_name': '1',
            'metrics': {
                'true_positive_rate': 1.0,
                'false_positive_rate': 0.14285714285714285,
                'precision': 0.75,
                'recall': 1.0,
                'f_measure': 0.8571428571428571,
            },
        },
        {
            'class_name': '2',
            'metrics': {
                'true_positive_rate': 0.3333333333333333,
                'false_positive_rate': 0.14285714285714285,
                'precision': 0.5,
                'recall': 0.3333333333333333,
                'f_measure': 0.4,
            },
        },
        {
            'class_name': '3',
            'metrics': {
                'true_positive_rate': 0.0,
                'false_positive_rate': 0.2222222222222222,
                'precision': 0.0,
                'recall': 0.0,
                'f_measure': 0.0,
            },
        },
    ],
    'global_metrics': {
        'f1': 0.6171428571428572,
        'accuracy': 0.6,
        'weighted_precision': 0.675,
        'weighted_recall': 0.6000000000000001,
        'weighted_true_positive_rate': 0.6000000000000001,
        'weighted_false_positive_rate': 0.10793650793650794,
        'weighted_f_measure': 0.6171428571428572,
        'confusion_matrix': [
            [2.0, 0.0, 1.0, 0.0],
            [0.0, 3.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 2.0],
            [0.0, 1.0, 0.0, 0.0],
        ],
    },
}

test_calculation_dataset_target_string_stats_res = {
    'categorical': 4,
    'datetime': 1,
    'duplicate_rows': 0,
    'duplicate_rows_perc': 0.0,
    'missing_cells': 3,
    'missing_cells_perc': 4.285714285714286,
    'n_observations': 10,
    'n_variables': 7,
    'numeric': 2,
}

test_calculation_dataset_target_string_dq_res = {
    'n_observations': 10,
    'class_metrics': [
        {'name': 'HEALTHY', 'count': 3, 'percentage': 30.0},
        {'name': 'ORPHAN', 'count': 1, 'percentage': 10.0},
        {'name': 'UNHEALTHY', 'count': 3, 'percentage': 30.0},
        {'name': 'UNKNOWN', 'count': 3, 'percentage': 30.0},
    ],
    'class_metrics_prediction': [
        {'name': 'HEALTHY', 'count': 4, 'percentage': 40.0},
        {'name': 'ORPHAN', 'count': 2, 'percentage': 20.0},
        {'name': 'UNHEALTHY', 'count': 2, 'percentage': 20.0},
        {'name': 'UNKNOWN', 'count': 2, 'percentage': 20.0},
    ],
    'feature_metrics': [
        {
            'feature_name': 'num1',
            'type': 'numerical',
            'missing_value': {'count': 1, 'percentage': 10.0},
            'mean': 1.1666666666666667,
            'std': 0.75,
            'min': 0.5,
            'max': 3.0,
            'median_metrics': {'perc_25': 1.0, 'median': 1.0, 'perc_75': 1.0},
            'class_median_metrics': [],
            'histogram': {
                'buckets': [
                    0.5,
                    0.75,
                    1.0,
                    1.25,
                    1.5,
                    1.75,
                    2.0,
                    2.25,
                    2.5,
                    2.75,
                    3.0,
                ],
                'reference_values': [2, 0, 5, 0, 1, 0, 0, 0, 0, 1],
            },
        },
        {
            'feature_name': 'num2',
            'type': 'numerical',
            'missing_value': {'count': 2, 'percentage': 20.0},
            'mean': 277.675,
            'std': 201.88635947695215,
            'min': 1.4,
            'max': 499.0,
            'median_metrics': {
                'perc_25': 117.25,
                'median': 250.0,
                'perc_75': 499.0,
            },
            'class_median_metrics': [],
            'histogram': {
                'buckets': [
                    1.4,
                    51.160000000000004,
                    100.92000000000002,
                    150.68000000000004,
                    200.44000000000003,
                    250.20000000000002,
                    299.96000000000004,
                    349.72,
                    399.48,
                    449.24,
                    499.0,
                ],
                'reference_values': [1, 1, 1, 1, 0, 0, 1, 0, 0, 3],
            },
        },
        {
            'feature_name': 'cat1',
            'type': 'categorical',
            'missing_value': {'count': 0, 'percentage': 0.0},
            'category_frequency': [
                {'name': 'B', 'count': 4, 'frequency': 0.4},
                {'name': 'C', 'count': 1, 'frequency': 0.1},
                {'name': 'A', 'count': 5, 'frequency': 0.5},
            ],
            'distinct_value': 3,
        },
        {
            'feature_name': 'cat2',
            'type': 'categorical',
            'missing_value': {'count': 0, 'percentage': 0.0},
            'category_frequency': [
                {'name': 'Y', 'count': 1, 'frequency': 0.1},
                {'name': 'X', 'count': 9, 'frequency': 0.9},
            ],
            'distinct_value': 2,
        },
    ],
}

test_calculation_dataset_target_string_mq_res = {
    'classes': ['HEALTHY', 'ORPHAN', 'UNHEALTHY', 'UNKNOWN'],
    'class_metrics': [
        {
            'class_name': 'HEALTHY',
            'metrics': {
                'true_positive_rate': 1.0,
                'false_positive_rate': 0.14285714285714285,
                'precision': 0.75,
                'recall': 1.0,
                'f_measure': 0.8571428571428571,
            },
        },
        {
            'class_name': 'ORPHAN',
            'metrics': {
                'true_positive_rate': 0.0,
                'false_positive_rate': 0.2222222222222222,
                'precision': 0.0,
                'recall': 0.0,
                'f_measure': 0.0,
            },
        },
        {
            'class_name': 'UNHEALTHY',
            'metrics': {
                'true_positive_rate': 0.6666666666666666,
                'false_positive_rate': 0.0,
                'precision': 1.0,
                'recall': 0.6666666666666666,
                'f_measure': 0.8,
            },
        },
        {
            'class_name': 'UNKNOWN',
            'metrics': {
                'true_positive_rate': 0.3333333333333333,
                'false_positive_rate': 0.14285714285714285,
                'precision': 0.5,
                'recall': 0.3333333333333333,
                'f_measure': 0.4,
            },
        },
    ],
    'global_metrics': {
        'f1': 0.6171428571428572,
        'accuracy': 0.6,
        'weighted_precision': 0.6749999999999999,
        'weighted_recall': 0.6000000000000001,
        'weighted_true_positive_rate': 0.6000000000000001,
        'weighted_false_positive_rate': 0.10793650793650793,
        'weighted_f_measure': 0.6171428571428572,
        'confusion_matrix': [
            [3.0, 0.0, 0.0, 0.0],
            [1.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 2.0, 1.0],
            [0.0, 2.0, 0.0, 1.0],
        ],
    },
}

test_calculation_dataset_perfect_classes_stats_res = {
    'categorical': 4,
    'datetime': 1,
    'duplicate_rows': 0,
    'duplicate_rows_perc': 0.0,
    'missing_cells': 3,
    'missing_cells_perc': 4.285714285714286,
    'n_observations': 10,
    'n_variables': 7,
    'numeric': 2,
}

test_calculation_dataset_perfect_classes_dq_res = {
    'n_observations': 10,
    'class_metrics': [
        {'name': 'HEALTHY', 'count': 4, 'percentage': 40.0},
        {'name': 'ORPHAN', 'count': 2, 'percentage': 20.0},
        {'name': 'UNHEALTHY', 'count': 2, 'percentage': 20.0},
        {'name': 'UNKNOWN', 'count': 2, 'percentage': 20.0},
    ],
    'class_metrics_prediction': [
        {'name': 'HEALTHY', 'count': 4, 'percentage': 40.0},
        {'name': 'ORPHAN', 'count': 2, 'percentage': 20.0},
        {'name': 'UNHEALTHY', 'count': 2, 'percentage': 20.0},
        {'name': 'UNKNOWN', 'count': 2, 'percentage': 20.0},
    ],
    'feature_metrics': [
        {
            'feature_name': 'num1',
            'type': 'numerical',
            'missing_value': {'count': 1, 'percentage': 10.0},
            'mean': 1.1666666666666667,
            'std': 0.75,
            'min': 0.5,
            'max': 3.0,
            'median_metrics': {'perc_25': 1.0, 'median': 1.0, 'perc_75': 1.0},
            'class_median_metrics': [],
            'histogram': {
                'buckets': [
                    0.5,
                    0.75,
                    1.0,
                    1.25,
                    1.5,
                    1.75,
                    2.0,
                    2.25,
                    2.5,
                    2.75,
                    3.0,
                ],
                'reference_values': [2, 0, 5, 0, 1, 0, 0, 0, 0, 1],
            },
        },
        {
            'feature_name': 'num2',
            'type': 'numerical',
            'missing_value': {'count': 2, 'percentage': 20.0},
            'mean': 277.675,
            'std': 201.88635947695215,
            'min': 1.4,
            'max': 499.0,
            'median_metrics': {
                'perc_25': 117.25,
                'median': 250.0,
                'perc_75': 499.0,
            },
            'class_median_metrics': [],
            'histogram': {
                'buckets': [
                    1.4,
                    51.160000000000004,
                    100.92000000000002,
                    150.68000000000004,
                    200.44000000000003,
                    250.20000000000002,
                    299.96000000000004,
                    349.72,
                    399.48,
                    449.24,
                    499.0,
                ],
                'reference_values': [1, 1, 1, 1, 0, 0, 1, 0, 0, 3],
            },
        },
        {
            'feature_name': 'cat1',
            'type': 'categorical',
            'missing_value': {'count': 0, 'percentage': 0.0},
            'category_frequency': [
                {'name': 'B', 'count': 4, 'frequency': 0.4},
                {'name': 'C', 'count': 1, 'frequency': 0.1},
                {'name': 'A', 'count': 5, 'frequency': 0.5},
            ],
            'distinct_value': 3,
        },
        {
            'feature_name': 'cat2',
            'type': 'categorical',
            'missing_value': {'count': 0, 'percentage': 0.0},
            'category_frequency': [
                {'name': 'Y', 'count': 1, 'frequency': 0.1},
                {'name': 'X', 'count': 9, 'frequency': 0.9},
            ],
            'distinct_value': 2,
        },
    ],
}

test_calculation_dataset_perfect_classes_mq_res = {
    'classes': ['HEALTHY', 'ORPHAN', 'UNHEALTHY', 'UNKNOWN'],
    'class_metrics': [
        {
            'class_name': 'HEALTHY',
            'metrics': {
                'true_positive_rate': 1.0,
                'false_positive_rate': 0.0,
                'precision': 1.0,
                'recall': 1.0,
                'f_measure': 1.0,
            },
        },
        {
            'class_name': 'ORPHAN',
            'metrics': {
                'true_positive_rate': 1.0,
                'false_positive_rate': 0.0,
                'precision': 1.0,
                'recall': 1.0,
                'f_measure': 1.0,
            },
        },
        {
            'class_name': 'UNHEALTHY',
            'metrics': {
                'true_positive_rate': 1.0,
                'false_positive_rate': 0.0,
                'precision': 1.0,
                'recall': 1.0,
                'f_measure': 1.0,
            },
        },
        {
            'class_name': 'UNKNOWN',
            'metrics': {
                'true_positive_rate': 1.0,
                'false_positive_rate': 0.0,
                'precision': 1.0,
                'recall': 1.0,
                'f_measure': 1.0,
            },
        },
    ],
    'global_metrics': {
        'f1': 1.0,
        'accuracy': 1.0,
        'weighted_precision': 1.0,
        'weighted_recall': 1.0,
        'weighted_true_positive_rate': 1.0,
        'weighted_false_positive_rate': 0.0,
        'weighted_f_measure': 1.0,
        'confusion_matrix': [
            [4.0, 0.0, 0.0, 0.0],
            [0.0, 2.0, 0.0, 0.0],
            [0.0, 0.0, 2.0, 0.0],
            [0.0, 0.0, 0.0, 2.0],
        ],
    },
}

test_calculation_dataset_with_nulls_res = {
    'classes': ['HEALTHY', 'ORPHAN', 'UNHEALTHY', 'UNKNOWN'],
    'class_metrics': [
        {
            'class_name': 'HEALTHY',
            'metrics': {
                'true_positive_rate': 1.0,
                'false_positive_rate': 0.16666666666666666,
                'precision': 0.6666666666666666,
                'recall': 1.0,
                'f_measure': 0.8,
            },
        },
        {
            'class_name': 'ORPHAN',
            'metrics': {
                'true_positive_rate': 0.0,
                'false_positive_rate': 0.2857142857142857,
                'precision': 0.0,
                'recall': 0.0,
                'f_measure': 0.0,
            },
        },
        {
            'class_name': 'UNHEALTHY',
            'metrics': {
                'true_positive_rate': 1.0,
                'false_positive_rate': 0.0,
                'precision': 1.0,
                'recall': 1.0,
                'f_measure': 1.0,
            },
        },
        {
            'class_name': 'UNKNOWN',
            'metrics': {
                'true_positive_rate': 0.3333333333333333,
                'false_positive_rate': 0.0,
                'precision': 1.0,
                'recall': 0.3333333333333333,
                'f_measure': 0.5,
            },
        },
    ],
    'global_metrics': {
        'f1': 0.6375,
        'accuracy': 0.625,
        'weighted_precision': 0.7916666666666666,
        'weighted_recall': 0.625,
        'weighted_true_positive_rate': 0.625,
        'weighted_false_positive_rate': 0.07738095238095238,
        'weighted_f_measure': 0.6375,
        'confusion_matrix': [
            [2.0, 0.0, 0.0, 0.0],
            [1.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 2.0, 0.0],
            [0.0, 2.0, 0.0, 1.0],
        ],
    },
}

test_calculation_dataset_indexing_res = {
    'classes': ['0', '1', '2', '3', '11'],
    'class_metrics': [
        {
            'class_name': '0',
            'metrics': {
                'true_positive_rate': 0.6666666666666666,
                'false_positive_rate': 0.0,
                'precision': 1.0,
                'recall': 0.6666666666666666,
                'f_measure': 0.8,
            },
        },
        {
            'class_name': '1',
            'metrics': {
                'true_positive_rate': 1.0,
                'false_positive_rate': 0.1111111111111111,
                'precision': 0.5,
                'recall': 1.0,
                'f_measure': 0.6666666666666666,
            },
        },
        {
            'class_name': '2',
            'metrics': {
                'true_positive_rate': 0.3333333333333333,
                'false_positive_rate': 0.14285714285714285,
                'precision': 0.5,
                'recall': 0.3333333333333333,
                'f_measure': 0.4,
            },
        },
        {
            'class_name': '3',
            'metrics': {
                'true_positive_rate': 0.0,
                'false_positive_rate': 0.2222222222222222,
                'precision': 0.0,
                'recall': 0.0,
                'f_measure': 0.0,
            },
        },
        {
            'class_name': '11',
            'metrics': {
                'true_positive_rate': 1.0,
                'false_positive_rate': 0.0,
                'precision': 1.0,
                'recall': 1.0,
                'f_measure': 1.0,
            },
        },
    ],
    'global_metrics': {
        'f1': 0.6266666666666667,
        'accuracy': 0.6,
        'weighted_precision': 0.7,
        'weighted_recall': 0.6000000000000001,
        'weighted_true_positive_rate': 0.6000000000000001,
        'weighted_false_positive_rate': 0.0761904761904762,
        'weighted_f_measure': 0.6266666666666667,
        'confusion_matrix': [
            [2.0, 0.0, 1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 2.0, 0.0],
            [0.0, 1.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 2.0],
        ],
    },
}
