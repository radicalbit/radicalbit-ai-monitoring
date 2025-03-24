import logging
from typing import TypeVar
import unittest

from sqlalchemy import text
from testcontainers.clickhouse import ClickHouseContainer

from app.core import get_config
from app.core.config import ClickHouseConfig
from app.db.clickhouse_database import ClickHouseBaseTable, ClickHouseDatabase
from app.db.tables.traces_table import Trace

T = TypeVar('T')

logger = logging.getLogger(get_config().log_config.logger_name)


class DatabaseIntegrationClickhouse(unittest.TestCase):
    container = None
    engine = None

    @classmethod
    def setUpClass(cls):
        cls.container = ClickHouseContainer(
            'clickhouse/clickhouse-server:latest',
            port=9000,
            username='default',
            password='default',
            dbname='default',
        )
        cls.container.start()
        cls.db_conf = ClickHouseConfig(
            clickhouse_db_host='localhost',
            clickhouse_db_port=cls.container.get_exposed_port(9000),
            clickhouse_db_user='default',
            clickhouse_db_pwd='default',
            clickhouse_db_name='default',
        )
        cls.db = ClickHouseDatabase(conf=cls.db_conf)
        cls.db.connect()
        ClickHouseBaseTable.metadata.create_all(cls.db._engine)

    def setUp(self):
        self.clean()

    @classmethod
    def tearDownClass(cls):
        # Stop container after all tests are complete
        if cls.container:
            cls.container.stop()
            cls.container = None
            cls.db = None

    def insert(self, table: list[T]) -> list[T]:
        with self.db.begin_session() as session:
            session.add_all(table)
            session.flush()
        return table

    def clean(self):
        with self.db.begin_session() as session:
            session.execute(text(f'TRUNCATE TABLE {Trace.__tablename__}'))
            session.commit()
