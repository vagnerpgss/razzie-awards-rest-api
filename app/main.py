from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database.connection import DatabaseManager
from app.routers import producers

_db_manager = DatabaseManager()

@asynccontextmanager
async def lifespan(_: FastAPI):
    _db_manager.initialize_database()
    yield

app = FastAPI(
    title="Razzie Awards API",
    description="API for accessing Razzie Awards data",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(producers.router, prefix="/api/v1", tags=["producers"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Razzie Awards API"}