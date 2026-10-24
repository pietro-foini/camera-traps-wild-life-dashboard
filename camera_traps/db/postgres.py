from pathlib import Path

import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine

SCRIPTS_DIR = Path(__file__).parent / "scripts"


class PostgresHandler:
    """PostgreSQL database handler implementation."""

    def __init__(self, db_user: str, db_password: str, db_host: str, db_port: str, db_name: str):
        """
        Initialize the database handler.

        :param db_user: database username
        :param db_password: database password
        :param db_host: database host address
        :param db_port: database port number
        :param db_name: database name
        """

        self.db_url = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        self.engine = create_engine(self.db_url, pool_pre_ping=True)

    def connect(self) -> None:
        """Connect to the database and verify connection status."""

        with self.engine.connect() as conn:
            conn.execute(sqlalchemy.text("SELECT 1"))

    def disconnect(self) -> None:
        """Disconnect from the database and dispose connection pool."""

        self.engine.dispose()

    def run_query(self, query: str, parameters: list | None = None) -> pd.DataFrame:
        """Run plain text query"""

        return pd.read_sql_query(sqlalchemy.text(query), self.engine, params=parameters, coerce_float=False)

    def run_sql_file(self, filename: str, parameters: list | None = None) -> pd.DataFrame:
        """Run SQL query and return results"""

        sql_path = SCRIPTS_DIR / filename
        query = sql_path.read_text(encoding="utf-8")
        return self.run_query(query, parameters=parameters)
