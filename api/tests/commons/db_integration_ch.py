import logging
from typing import TypeVar
import unittest

from sqlalchemy import text
from testcontainers.clickhouse import ClickHouseContainer

from app.core import get_config
from app.core.config import ClickHouseConfig
from app.db.database import ClickHouseBaseTable, Database, DatabaseDialect
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
            db_host_ch='localhost',
            db_port_ch=cls.container.get_exposed_port(9000),
            db_user_ch='default',
            db_pwd_ch='default',
            db_name_ch='default',
        )
        cls.db = Database(dialect=DatabaseDialect.CLICKHOUSE, conf=cls.db_conf)

    def setUp(self):
        self.db.connect()
        with self.db._engine.connect() as conn:
            conn.commit()
        ClickHouseBaseTable.metadata.create_all(self.db._engine)

    def tearDown(self):
        self.container.stop()
        self.container = None
        self.engine = None
        self.session = None

    def insert(self, table: list[T]) -> list[T]:
        with self.db.begin_session() as session:
            session.add_all(table)
            session.flush()
        return table

    def clean(self):
        with self.db.begin_session() as session:
            session.execute(text(f'TRUNCATE TABLE {Trace.__tablename__}'))
            session.commit()
