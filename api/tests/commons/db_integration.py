import unittest

import testing.postgresql

from app.core.config import DBConfig
from app.db import database
from app.db.database import Database, DatabaseDialect

Postgresql = testing.postgresql.PostgresqlFactory(cache_initialized_db=True)


class DatabaseIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.db_conf = DBConfig()
        cls.db = Database(dialect=DatabaseDialect.POSTGRES, conf=cls.db_conf)

    def setUp(self):
        self.postgresql = Postgresql()
        self.db._db_url = self.postgresql.url()
        self.db.connect()
        with self.db._engine.connect() as conn:
            conn.commit()
        database.BaseTable.metadata.create_all(self.db._engine)
        self.db.init_mappings()

    def tearDown(self):
        database.BaseTable.metadata.drop_all(self.db._engine)
        self.db.reset_connection()
        self.postgresql.stop()
