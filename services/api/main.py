import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from services.api.db import initialize_pool, close_pool
from services.analytics.queries import (
    total_events,
    total_revenue,
    events_by_product,
    revenue_by_product,
    event_distribution,
)

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
        count = total_events()
        return {"total_events": count}
    except Exception as e:
        logger.error(f"Error fetching event count: {e}")
        return {"error": "Failed to fetch event count", "total_events": 0}

@app.get("/analytics/top-products")
def top_products():
    """Get top products by event count."""
    try:
        products = events_by_product()
        return products
    except Exception as e:
        logger.error(f"Error fetching top products: {e}")
        return {"error": "Failed to fetch top products"}

@app.get("/analytics/revenue")
def revenue():
    """Get total revenue from purchase events."""
    try:
        rev = total_revenue()
        return {"total_revenue": rev}
    except Exception as e:
        logger.error(f"Error fetching revenue: {e}")
        return {"error": "Failed to fetch revenue", "total_revenue": 0}

@app.get("/analytics/revenue-by-product")
def revenue_by_product_endpoint():
    """Get total revenue grouped by product."""
    try:
        revenue = revenue_by_product()
        return revenue
    except Exception as e:
        logger.error(f"Error fetching revenue by product: {e}")
        return {"error": "Failed to fetch revenue by product"}

@app.get("/analytics/event-distribution")
def event_distribution_endpoint():
    """Get event count grouped by event type."""
    try:
        distribution = event_distribution()
        return distribution
    except Exception as e:
        logger.error(f"Error fetching event distribution: {e}")
        return {"error": "Failed to fetch event distribution"}