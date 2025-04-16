import pytest
from pathlib import Path
from app.database.connection import DatabaseManager
import duckdb


@pytest.fixture
def test_db(tmp_path):
    test_csv = Path(__file__).parent / "test_data" / "test_movielist.csv"

    with DatabaseManager(
            db_path=str(tmp_path / "test.db"),
            csv_path=str(test_csv)
    ) as db:
        db.initialize_database()
        yield db

@pytest.fixture(autouse=True)
def clean_duckdb_state():
    """
    Fixture to ensure DuckDB connections are reset before each test.
    This helps avoid cross-test contamination when using :memory: DBs or default sessions.
    """
    yield
    duckdb.close()