import logging

import clickhouse_sqlalchemy as ch_alchemy
from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.declarative import DeferredReflection
from sqlalchemy.orm import Session

from app.core import get_config
from app.core.config import ClickHouseConfig

logger = logging.getLogger(get_config().log_config.logger_name)


class Reflected(DeferredReflection):
    __abstract__ = True


ClickHouseBaseTable = ch_alchemy.get_declarative_base(
    metadata=MetaData(schema='default')
)


class ClickHouseDatabase:
    def __init__(self, conf: ClickHouseConfig):
        self._db_url = f'clickhouse+native://{conf.clickhouse_db_user}:{conf.clickhouse_db_pwd}@{conf.clickhouse_db_host}:{conf.clickhouse_db_port}/{conf.clickhouse_db_name}'
        self._engine = None
        self._SessionFactory = None
        self._connected = False

    def connect(self):
        logger.info('Trying to connect to Clickhouse DB')
        if not self._connected:
            logger.info('Connecting to the Clickhouse DB')
            self._engine = create_engine(self._db_url)
            self._connected = True
        else:
            logger.warning('Not connecting. Connection with the DB already established')

    def reset_connection(self):
        logger.info('Resetting DB connection')
        self._engine = None
        self._SessionFactory = None
        self._connected = False

    def init_mappings(self):
        logger.info('Initiating DB orm mappings')
        Reflected.prepare(self._engine)

    def begin_session(self) -> Session:
        return ch_alchemy.make_session(self._engine)

    @property
    def db_url(self):
        return self._db_url
