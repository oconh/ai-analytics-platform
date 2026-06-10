import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from services.api.db import initialize_pool, close_pool, get_db_connection

logger = logging.getLogger(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle: startup and shutdown."""
    # Startup
    logger.info("Starting FastAPI application")
    initialize_pool()
    yield
    # Shutdown
    logger.info("Shutting down FastAPI application")
    close_pool()


app = FastAPI(title="Analytics API", version="1.0.0", lifespan=lifespan)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/events/count")
def get_event_count():
    """Get total count of events in the database."""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) FROM events;")
                result = cur.fetchone()[0]
                return {"total_events": result}
    except Exception as e:
        logger.error(f"Error fetching event count: {e}")
        return {"error": "Failed to fetch event count", "total_events": 0}

@app.get("/analytics/top-products")
def top_products():
    """Get top products by event count."""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT product, COUNT(*) as count
                    FROM events
                    GROUP BY product
                    ORDER BY count DESC;
                """)
                result = cur.fetchall()
                return [
                    {"product": row[0], "count": row[1]}
                    for row in result
                ]
    except Exception as e:
        logger.error(f"Error fetching top products: {e}")
        return {"error": "Failed to fetch top products"}

@app.get("/analytics/revenue")
def revenue():
    """Get total revenue from purchase events."""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT SUM(price)
                    FROM events
                    WHERE event_type = 'purchase';
                """)
                result = cur.fetchone()[0] or 0
                return {"total_revenue": float(result)}
    except Exception as e:
        logger.error(f"Error fetching revenue: {e}")
        return {"error": "Failed to fetch revenue", "total_revenue": 0}