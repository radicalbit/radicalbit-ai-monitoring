import logging

from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.declarative import DeferredReflection
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from app.core import get_config
from app.core.config import DBConfig
from app.db.custom_query import CustomQuery

logger = logging.getLogger(get_config().log_config.logger_name)


class Reflected(DeferredReflection):
    __abstract__ = True


BaseTable = declarative_base(metadata=MetaData(schema=get_config().db_config.db_schema))


class Database:
    def __init__(self, conf: DBConfig):
        self._db_url = f'postgresql+psycopg2://{conf.db_user}:{conf.db_pwd}@{conf.db_host}:{conf.db_port}/{conf.db_name}'
        self._engine = None
        self._SessionFactory = None
        self._connected = False

    def connect(self):
        logger.info('Trying to connect to the DB')
        if not self._connected:
            logger.info('Connecting to the DB')
            self._engine = create_engine(self._db_url, pool_pre_ping=True)
            self._SessionFactory = sessionmaker(
                bind=self._engine,
                future=True,
                expire_on_commit=False,
                query_cls=CustomQuery,
            )
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
        return self._SessionFactory.begin()

    @property
    def db_url(self):
        return self._db_url
