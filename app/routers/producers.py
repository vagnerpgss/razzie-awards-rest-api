from fastapi import APIRouter, Depends, HTTPException
from app.database.connection import get_connection_db
from app.services.producer_service import calculate_producer_intervals
from app.schemas.producers import ProducerIntervalResponse
import duckdb

router = APIRouter()

@router.get("/intervals", response_model=ProducerIntervalResponse)
def get_producers_with_intervals(db: duckdb.DuckDBPyConnection = Depends(get_connection_db)):
    response = calculate_producer_intervals(db)
    if not response.min and not response.max:
        raise HTTPException(status_code=404, detail="No producer intervals found.")
    return response