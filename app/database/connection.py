import duckdb
import pandas as pd
from pathlib import Path
from typing import Generator

class DatabaseManager:
    def __init__(self, db_path: str = ":memory:", csv_path: str = None):
        self.db_path = db_path
        self._csv_path = csv_path
        self.conn = None

    @property
    def csv_path(self):
        return self._csv_path or str(Path(__file__).parent.parent.parent / 'data' / 'Movielist.csv')

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def connect(self):
        if not self.conn:
            self.conn = duckdb.connect(database=self.db_path)
        return self.conn

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None

    def initialize_database(self):
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
        csv_file = Path(self.csv_path)
        if not csv_file.exists():
            raise FileNotFoundError(
                f"Movie Awards DB: CSV file not found at {csv_file.absolute()}"
            )

        df = pd.read_csv(csv_file, sep=';')
        df['winner'] = df['winner'].fillna('').apply(
            lambda x: x.strip().lower() == 'yes'
        )

        self.conn.execute("DELETE FROM worst_movie_nominations;")
        self.conn.register('input_df', df)
        self.conn.execute("""
            INSERT INTO worst_movie_nominations 
            SELECT year, title, studios, producers, winner FROM input_df;
        """)

    def _create_indexes(self):
        self.conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_producer 
            ON worst_movie_nominations(producers);
        """)
        self.conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_year 
            ON worst_movie_nominations(year);
        """)

def get_db() -> Generator:
    with DatabaseManager() as db:
        db.initialize_database()
        yield db.conn