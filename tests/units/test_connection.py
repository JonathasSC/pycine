import os
import sqlite3
import pytest
from src.database.conn import Connection


class TestConnection:

    # Config Teardown
    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        self.db_name = 'test.db'
        self.conn: Connection = Connection(self.db_name)
        self.conn.connect()

        yield

        self.conn.close()

        if os.path.exists(self.db_name):
            os.remove(self.db_name)

    def test_connect(self):
        assert isinstance(self.conn.connection, sqlite3.Connection)
        assert self.conn.connection is not None

    def test_create_database(self):
        assert os.path.exists(self.db_name)

    def test_close(self):
        self.conn.close()
        assert self.conn.connection is None
