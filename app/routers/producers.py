from fastapi import APIRouter, Depends, HTTPException
from app.database.connection import get_connection_db
from app.services.producer_service import calculate_producer_intervals
from app.schemas.producers import ProducerIntervalResponse
import duckdb
import logging

# Initialize the API router for producer-related endpoints
router = APIRouter()

@router.get("/producers/intervals", response_model=ProducerIntervalResponse)
def get_producers_with_intervals(db: duckdb.DuckDBPyConnection = Depends(get_connection_db)):
    """
    Retrieve the producers with the shortest and longest award intervals.

    This endpoint queries the database to find producers who have won multiple times,
    and calculates the time intervals between their wins. If no interval data is found,
    it returns a 404 error. If any unexpected error occurs, it returns a 500 error with
    a generic error message.

    Args:
        db (duckdb.DuckDBPyConnection): A DuckDB connection instance provided via FastAPI dependency injection.

    Returns:
        ProducerIntervalResponse: A response containing the producers with minimum and maximum intervals.

    Raises:
        HTTPException: 404 if no data found, 500 if an unexpected error occurs.
    """
    try:
        # Call the service function to calculate the producer intervals
        response = calculate_producer_intervals(db)

        # If both lists are empty, raise 404
        if not response.min and not response.max:
            raise HTTPException(status_code=404, detail="No producer intervals found.")

        return response

    except HTTPException:
        # Let FastAPI handle explicitly raised HTTPExceptions
        raise

    except Exception as e:
        # Log the unexpected error for debugging purposes
        logging.exception("Unexpected error while calculating producer intervals")
        raise HTTPException(status_code=500, detail="Internal server error.")
