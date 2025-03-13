from typing import TypeVar
import unittest

from app.core.config import ClickHouseConfig, DBConfig
from app.db import database
from app.db.database import Database, DatabaseDialect

T = TypeVar('T')


class DatabaseIntegrationCh(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.db_conf = DBConfig()
        cls.ch_db_conf = ClickHouseConfig()
        cls.ch_db = Database(dialect=DatabaseDialect.CLICKHOUSE, conf=cls.ch_db_conf)

    def setUp(self):
        self.ch_db.connect()
        with self.ch_db._engine.connect() as conn:
            conn.commit()
        database.BaseTable.metadata.create_all(self.ch_db._engine)
        self.ch_db.init_mappings()

    def tearDownCh(self):
        database.BaseTable.metadata.drop_all(self.ch_db._engine)
        self.ch_db.reset_connection()

    def insert(self, table: T) -> T:
        with self.ch_db.begin_session() as session:
            session.add(table)
            session.flush()
            return table
