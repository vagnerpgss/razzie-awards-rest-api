from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database.connection import DatabaseManager
from app.routers import producers

# Instantiate the database manager.
# Responsible for setting up and managing the database connection.
_db_manager = DatabaseManager()

@asynccontextmanager
async def lifespan(_: FastAPI):
    """
    Manages the application lifespan.

    Initializes the database when the application starts.
    You can expand this to close connections or clean up resources on shutdown if needed.
    """
    _db_manager.initialize_database()
    yield # Control is passed to the app runtime here
    # _db_manager.close() could be called here if a close method is implemented.

# Create the FastAPI app instance with metadata and lifespan context.
app = FastAPI(
    title="Razzie Awards API",
    description="API for accessing Razzie Awards data",
    version="1.0.0",
    lifespan=lifespan
)

# Register the producers router under the "/api/v1" prefix.
app.include_router(producers.router, prefix="/api/v1", tags=["producers"])

@app.get("/")
async def root():
    """
    Root endpoint.

    Returns a welcome message when accessing the root path ("/").
    """
    return {"message": "Welcome to the Razzie Awards API"}