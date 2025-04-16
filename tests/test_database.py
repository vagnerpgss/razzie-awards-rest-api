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


def test_data_types(clean_duckdb_state, tmp_path):
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

def test_missing_csv_handling(tmp_path):
    """
    Test that DatabaseManager raises FileNotFoundError when CSV path does not exist.
    """
    fake_csv = tmp_path / "non_existent.csv"

    db = DatabaseManager(
        db_path=str(tmp_path / "test_non_existent.db"),
        csv_path=str(fake_csv)
    )

    with pytest.raises(FileNotFoundError):
        db.initialize_database()

def test_empty_table_returns_empty_response():
    """
    Test that when the table is empty, the service returns an empty response
    without raising exceptions.
    """
    import duckdb
    from app.services.producer_service import calculate_producer_intervals

    db = duckdb.connect(database=":memory:")
    db.execute("""
        CREATE TABLE worst_movie_nominations (
            year INTEGER,
            producers VARCHAR,
            winner BOOLEAN
        )
    """)

    result = calculate_producer_intervals(db)

    assert result.min == []
    assert result.max == []

def test_producer_with_one_win_only():
    """
    Test that a producer with only one win is not included in interval calculations.
    """
    import duckdb
    from app.services.producer_service import calculate_producer_intervals

    db = duckdb.connect(database=":memory:")
    db.execute("""
        CREATE TABLE worst_movie_nominations (
            year INTEGER,
            producers VARCHAR,
            winner BOOLEAN
        )
    """)
    db.execute("INSERT INTO worst_movie_nominations VALUES (2000, 'Solo Producer', TRUE)")

    result = calculate_producer_intervals(db)

    # A single win should not generate an interval
    assert result.min == []
    assert result.max == []

def test_loading_empty_csv(tmp_path):
    """
    Test that loading an empty CSV file results in zero records in the table.
    """
    empty_csv = tmp_path / "empty.csv"
    empty_csv.write_text("year;title;studios;producers;winner\n")  # Only header

    with DatabaseManager(
            db_path=":memory:",
            csv_path=str(empty_csv)
    ) as db:
        db.initialize_database()

        result = db.conn.execute("SELECT COUNT(*) FROM worst_movie_nominations;").fetchone()
        assert result[0] == 0, "Expected 0 records when loading an empty CSV file"

def test_winner_field_normalization(tmp_path):
    """
    Test that the 'winner' field is correctly normalized regardless of case or whitespace.
    """
    csv_content = """year;title;studios;producers;winner
1982;My movie 1;Studio A;Producer X; Yes
1982;My movie 2;Studio B;Producer Y;YES
1982;My movie 3;Studio C;Producer Z; yes 
1982;My movie 4;Studio Z;Producer Z;no
"""
    test_csv = tmp_path / "normalized_winner.csv"
    test_csv.write_text(csv_content)

    with DatabaseManager(
            db_path=":memory:",
            csv_path=str(test_csv)
    ) as db:
        db.initialize_database()

        winners = db.conn.execute("""
            SELECT COUNT(*) FROM worst_movie_nominations 
            WHERE winner = true;
        """).fetchone()[0]

        assert winners == 3, "Expected 3 normalized winners regardless of formatting"