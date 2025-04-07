from fastapi import FastAPI
from contextlib import asynccontextmanager
from pathlib import Path
from app.database.connection import DatabaseManager


@asynccontextmanager
async def lifespan(_: FastAPI):
    db_path = Path(":memory:")
    csv_path = Path(__file__).parent.parent / "data" / "Movielist.csv"

    with DatabaseManager(
        db_path=str(db_path),
        csv_path=str(csv_path)
    ) as db:
        db.initialize_database()

    yield


app = FastAPI(
    title="Razzie Awards API",
    description="API for accessing Razzie Awards data",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/")
async def root():
    return {"message": "Welcome to the Razzie Awards API"}