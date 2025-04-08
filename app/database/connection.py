import duckdb
import pandas as pd
from pathlib import Path
from typing import Generator

class DatabaseManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
        return cls._instance

    def __init__(self, db_path: str = ":memory:", csv_path: str = None):
        if hasattr(self, '_initialized') and self._initialized:
            return

        self.db_path = db_path
        self.csv_path = csv_path or str(Path(__file__).parent.parent.parent / 'data' / 'Movielist.csv')
        self.conn = None
        self._initialized = True

    def connect(self):
        if not self.conn:
            self.conn = duckdb.connect(database=self.db_path)
        return self.conn

    def get_connection(self):
        return self.connect()

    def initialize_database(self):
        self.connect()
        self._create_tables()
        self._load_initial_data()
        self._create_indexes()

    def _create_tables(self):
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
        df = pd.read_csv(self.csv_path, sep=';')
        df['winner'] = df['winner'].fillna('').apply(lambda x: x.strip().lower() == 'yes')

        self.conn.execute("DELETE FROM worst_movie_nominations;")
        self.conn.register('input_df', df)
        self.conn.execute("""
            INSERT INTO worst_movie_nominations 
            SELECT year, title, studios, producers, winner FROM input_df;
        """)

    def _create_indexes(self):
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_producer ON worst_movie_nominations(producers);")
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_year ON worst_movie_nominations(year);")

def get_connection_db() -> Generator:
    db_manager = DatabaseManager()
    yield db_manager.get_connection()