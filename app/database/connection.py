import os

import duckdb
import pandas as pd
from pathlib import Path
from typing import Generator
from pandas.errors import EmptyDataError


class DatabaseManager:
    """
    Singleton class to manage a DuckDB connection, create tables,
    load initial data from a CSV file, and manage the database lifecycle.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        # Ensure only one instance of the class is created (Singleton pattern)
        if not cls._instance:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
        return cls._instance

    def __init__(self, db_path: str = ":memory:", csv_path: str = None):
        """
        Initialize the database manager.

        Args:
            db_path (str): Path to the DuckDB database file. Defaults to in-memory DB.
            csv_path (str): Optional path to the CSV file to preload data from.
        """
        # Avoid reinitialization if already initialized, but allow it in tests
        if not os.getenv("PYTEST_CURRENT_TEST") and hasattr(self, '_initialized') and self._initialized:
            return

        self.db_path = db_path
        self.csv_path = str(csv_path) if csv_path else str(Path(__file__).parent.parent.parent / 'data' / 'Movielist.csv')

        self.conn = None
        self._initialized = True

    def __enter__(self):
        """Enable usage with the 'with' statement, opening the connection on enter."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Ensure connection is properly closed on exiting the 'with' block."""
        if self.conn:
            self.conn.close()
            self.conn = None

    def close(self):
        """Close the current database connection if it exists."""
        if self.conn:
            self.conn.close()
            self.conn = None

    def connect(self):
        """
        Connect to the DuckDB database, creating a connection if not already active.

        Returns:
            duckdb.DuckDBPyConnection: Active database connection.
        """
        if not self.conn:
            self.conn = duckdb.connect(database=self.db_path)
        return self.conn

    def get_connection(self):
        """
        Retrieve the current active connection, creating it if necessary.

        Returns:
            duckdb.DuckDBPyConnection: Active database connection.
        """
        return self.connect()

    def initialize_database(self):
        """
        Initialize the database by creating tables, loading initial data, and creating indexes.
        """
        self.connect()
        self._create_tables()
        self._load_initial_data()
        self._create_indexes()

    def _create_tables(self):
        """Create the 'worst_movie_nominations' table if it doesn't exist."""
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS worst_movie_nominations (
                year INTEGER,
                title TEXT,
                studios TEXT,
                producers TEXT,
                winner BOOLEAN
            );
        """)

    def _load_initial_data(self):
        """
        Load movie nominations from the CSV file into the database.
        Converts the 'winner' field to a boolean value.
        Skips loading if the CSV is empty or has no data rows.
        """
        try:
            df = pd.read_csv(self.csv_path, sep=';', engine='python')
        except FileNotFoundError:
            raise FileNotFoundError(f"Movie Awards DB: CSV file not found at '{self.csv_path}'")
        except EmptyDataError:
            # Log or silently skip loading data if file is empty
            return

        if df.empty:
            return

        # Convert 'winner' column to boolean
        df['winner'] = df['winner'].fillna('').apply(lambda x: x.strip().lower() == 'yes')

        # Clear existing data and insert new records
        self.conn.execute("DELETE FROM worst_movie_nominations;")
        self.conn.register('input_df', df)
        self.conn.execute("""
            INSERT INTO worst_movie_nominations 
            SELECT year, title, studios, producers, winner FROM input_df;
        """)

    def _create_indexes(self):
        """Create indexes on relevant columns to improve query performance."""
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_producer ON worst_movie_nominations(producers);")
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_year ON worst_movie_nominations(year);")


def get_connection_db() -> Generator:
    """
    Generator function to yield a DuckDB connection managed by DatabaseManager.

    Yields:
        duckdb.DuckDBPyConnection: An active DuckDB connection.
    """
    db_manager = DatabaseManager()
    yield db_manager.get_connection()
