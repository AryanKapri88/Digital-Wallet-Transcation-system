import logging
from fastapi import FastAPI
from app.database import Base, engine
from app.routers import user, transaction

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Include routers
app.include_router(user.router)
app.include_router(transaction.router)

# Create database tables
def create_tables():
    for attempt in range(3):
        try:
            logger.info(f"Creating database tables (attempt {attempt + 1}/3)...")
            Base.metadata.create_all(bind=engine)
            logger.info("Database tables created successfully.")
            break
        except Exception as e:
            logger.error(f"Error creating tables: {e}")
            if attempt == 2:
                raise

if __name__ == "__main__":
    import uvicorn
    import sys
    logger.info(f"sys.path: {sys.path}")
    logger.info("Starting server at http://127.0.0.1:8000")
    create_tables()
    uvicorn.run(app, host="127.0.0.1", port=8000)