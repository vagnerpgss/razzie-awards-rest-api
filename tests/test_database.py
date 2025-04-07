import pytest
from pathlib import Path
from app.database.connection import DatabaseManager


def test_lifecycle(tmp_path):
    test_csv = Path(__file__).parent / "test_data" / "test_movielist.csv"

    with DatabaseManager(
            db_path=":memory:",
            csv_path=str(test_csv)
    ) as db:
        db.initialize_database()

        assert db.conn is not None
        assert db.conn.execute("SELECT 1").fetchone() == (1,)

        result = db.conn.execute("""
            SELECT COUNT(*) AS total,
                   SUM(CASE WHEN winner THEN 1 ELSE 0 END) AS winners
            FROM worst_movie_nominations;
        """).fetchone()

        assert result[0] == 20, "Must have 20 records from test CSV"
        assert result[1] == 3, "Must have 3 winners in test data"


def test_connection_management(tmp_path):
    db = DatabaseManager(db_path=str(tmp_path / "test.db"))

    assert db.conn is None
    db.connect()
    assert db.conn is not None
    db.close()
    assert db.conn is None


def test_missing_csv_handling():
    invalid_path = "non_existent.csv"

    with pytest.raises(FileNotFoundError) as exc_info:
        with DatabaseManager(csv_path=invalid_path) as db:
            db.initialize_database()

    assert str(invalid_path) in str(exc_info.value), \
        "Error message should mention the missing CSV path"
    assert "Movie Awards DB" in str(exc_info.value), \
        "Error should be identified as coming from our DB system"


def test_index_creation(tmp_path):
    test_csv = Path(__file__).parent / "test_data" / "test_movielist.csv"

    with DatabaseManager(
            db_path=":memory:",
            csv_path=str(test_csv)
    ) as db:
        db.initialize_database()

        indexes = db.conn.execute("""
            SELECT index_name 
            FROM duckdb_indexes 
            WHERE table_name = 'worst_movie_nominations';
        """).fetchall()

        index_names = {idx[0] for idx in indexes}
        assert 'idx_producer' in index_names
        assert 'idx_year' in index_names


def test_data_types(tmp_path):
    test_csv = Path(__file__).parent / "test_data" / "test_movielist.csv"

    with DatabaseManager(
            db_path=str(tmp_path / "test.db"),
            csv_path=str(test_csv)
    ) as db:
        db.initialize_database()

        columns = db.conn.execute("""
            DESCRIBE SELECT * FROM worst_movie_nominations;
        """).fetchall()

        expected_types = {
            'year': 'INTEGER',
            'title': 'VARCHAR',
            'studios': 'VARCHAR',
            'producers': 'VARCHAR',
            'winner': 'BOOLEAN'
        }

        for col_info in columns:
            col_name = col_info[0]
            duckdb_type = col_info[1]

            normalized_type = duckdb_type.replace('TEXT', 'VARCHAR')

            assert normalized_type == expected_types[col_name], \
                f"Column {col_name}: expected {expected_types[col_name]}, got {duckdb_type}"