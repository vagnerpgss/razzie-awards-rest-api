from pydantic import BaseModel
from typing import List

class ProducerInterval(BaseModel):
    """
    Represents the interval between two award wins for a producer.

    Attributes:
        producer (str): Name of the producer.
        interval (int): Number of years between two consecutive wins.
        previousWin (int): Year of the earlier win.
        followingWin (int): Year of the later win.
    """
    producer: str
    interval: int
    previousWin: int
    followingWin: int

class ProducerIntervalResponse(BaseModel):
    """
    Response model containing producers with minimum and maximum award intervals.

    Attributes:
        min (List[ProducerInterval]): List of producers with the shortest intervals between wins.
        max (List[ProducerInterval]): List of producers with the longest intervals between wins.
    """
    min: List[ProducerInterval]
    max: List[ProducerInterval]
