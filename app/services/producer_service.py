from collections import defaultdict
from typing import List
import duckdb
from app.schemas.producers import ProducerInterval, ProducerIntervalResponse

def calculate_producer_intervals(db: duckdb.DuckDBPyConnection) -> ProducerIntervalResponse:
    query = """
        SELECT year, producers 
        FROM worst_movie_nominations 
        WHERE winner = TRUE AND producers IS NOT NULL AND producers <> '';
    """
    result = db.execute(query).fetchall()

    producer_years = defaultdict(list)

    for year, producers_str in result:
        producers = [p.strip() for p in producers_str.split(',') if p.strip()]
        for producer in producers:
            producer_years[producer].append(year)

    intervals: List[ProducerInterval] = []

    for producer, years in producer_years.items():
        sorted_years = sorted(set(years))
        for i in range(1, len(sorted_years)):
            interval = sorted_years[i] - sorted_years[i-1]
            intervals.append(ProducerInterval(
                producer=producer,
                interval=interval,
                previousWin=sorted_years[i-1],
                followingWin=sorted_years[i]
            ))

    if not intervals:
        return ProducerIntervalResponse(min=[], max=[])

    min_interval = min(i.interval for i in intervals)
    max_interval = max(i.interval for i in intervals)

    min_intervals = [i for i in intervals if i.interval == min_interval]
    max_intervals = [i for i in intervals if i.interval == max_interval]

    return ProducerIntervalResponse(min=min_intervals, max=max_intervals)