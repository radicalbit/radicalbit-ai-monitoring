logger_config = {
    "logger_name": "radicalbit-ai-monitoring-spark",
    "log_format": "%(levelname)s | %(asctime)s | %(message)s",
    "log_level": "DEBUG",
    "formatters": {
        "default": {
            "format": "%(levelname)s | %(asctime)s | %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        }
    },
    "loggers": {
        "logger_name": {
            "handlers": ["default"],
            "level": "DEBUG",
            "propagate": False,
        }
    },
}
