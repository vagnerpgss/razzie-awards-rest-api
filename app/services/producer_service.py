from collections import defaultdict
from typing import List
import duckdb
import re
from app.schemas.producers import ProducerInterval, ProducerIntervalResponse


def calculate_producer_intervals(db: duckdb.DuckDBPyConnection) -> ProducerIntervalResponse:
    """
    Calculate the shortest and longest award intervals for producers.

    This function queries a database table (`worst_movie_nominations`) to find all producers
    who have won more than once. It then calculates the interval in years between each pair
    of consecutive wins for each producer. Finally, it identifies the producers with the
    shortest and longest intervals.

    Args:
        db (duckdb.DuckDBPyConnection): A DuckDB connection instance.

    Returns:
        ProducerIntervalResponse: A response model containing lists of producers with the
        shortest and longest intervals between awards.
    """
    query = """
        SELECT year, producers 
        FROM worst_movie_nominations 
        WHERE winner = TRUE AND producers IS NOT NULL AND producers <> '';
    """

    # Execute the query and fetch all rows
    result = db.execute(query).fetchall()

    # Dictionary to collect all winning years for each producer
    producer_years = defaultdict(list)

    for year, producers_str in result:
        # Split producer names by comma or ' and ', and strip whitespace
        producers = [p.strip() for p in re.split(r',|\s+and\s+', producers_str) if p.strip()]
        for producer in producers:
            producer_years[producer].append(int(year))

    intervals: List[ProducerInterval] = []

    # Calculate intervals between consecutive wins for each producer
    for producer, years in producer_years.items():
        sorted_years = sorted(set(years))  # Remove duplicates and sort
        for i in range(1, len(sorted_years)):
            interval = sorted_years[i] - sorted_years[i - 1]
            intervals.append(ProducerInterval(
                producer=producer,
                interval=interval,
                previousWin=sorted_years[i - 1],
                followingWin=sorted_years[i]
            ))

    # If no valid intervals were found, return empty response
    if not intervals:
        return ProducerIntervalResponse(min=[], max=[])

    # Identify the smallest and largest intervals
    min_interval = min(i.interval for i in intervals)
    max_interval = max(i.interval for i in intervals)

    # Collect all intervals matching the min and max
    min_intervals = [i for i in intervals if i.interval == min_interval]
    max_intervals = [i for i in intervals if i.interval == max_interval]

    return ProducerIntervalResponse(min=min_intervals, max=max_intervals)
