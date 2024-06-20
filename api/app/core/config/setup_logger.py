from logging.config import dictConfig

from app.core.config.config import get_config

# setup loggers
dictConfig(get_config().log_config.model_dump())
