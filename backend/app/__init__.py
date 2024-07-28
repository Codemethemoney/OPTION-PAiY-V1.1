"""
This module initializes and configures the FastAPI application for the OPTION_PAY_AGENTS API.
"""

import logging
import time
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.api import router as api_router
from app.core.config import settings
from app.core.logging import setup_logging
from app.db import engine, SessionLocal, Base
from app.middlewares.authentication import authentication_middleware
from app.middlewares.request_id import request_id_middleware
from app.utils.rate_limit import SlidingWindowRateLimiter
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import sentry_sdk
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from starlette_exporter import PrometheusMiddleware, handle_metrics
from redis import Redis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_versioning import VersionedFastAPI
from alembic import command
from alembic.config import Config
from app.utils.tasks import create_task

# Set up logging
logger = logging.getLogger(__name__)

# Create database tables if they don't exist
def init_db():
    Base.metadata.create_all(bind=engine)

# Close the database connection pool
def close_db():
    engine.dispose()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for the FastAPI application.
    Handles startup and shutdown events.
    """
    # Startup
    setup_logging()
    init_db()
    redis = Redis.from_url(settings.REDIS_URL, encoding="utf-8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

    # Shutdown
    await close_db()
    await close_caches()


def create_app() -> FastAPI:
    """
    Creates and configures the FastAPI application.
    """

    app = FastAPI(
        title=settings.PROJECT_NAME,
        description=settings.PROJECT_DESCRIPTION,
        version=__version__,
        lifespan=lifespan,
        docs_url=None,   # Disable default docs
        redoc_url=None,
    )

    # Set up CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Rate limiting middleware
    limiter = Limiter(key_func=get_remote_address, default_limits=["10/minute"])
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    # Add middleware to the app
    app.add_middleware(authentication_middleware)
    app.add_middleware(request_id_middleware)
    app.add_middleware(PrometheusMiddleware)

    # Include API routes
    app.include_router(api_router, prefix="/api")

    # Add API versioning using fastapi-versioning
    app = VersionedFastAPI(app, 
                          version_format='{major}', 
                          prefix_format='/v{major}', 
                          enable_latest=True)

    # Adding metrics endpoint
    app.add_route("/metrics", handle_metrics)

    # Initialize Sentry for error tracking (configure your DSN)
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        integrations=[SentryAsgiMiddleware(app)],
        traces_sample_rate=1.0,
        environment=settings.ENVIRONMENT
    )
    logger.info("Sentry integration initialized")
    return app


# Creating the application instance
app = create_app()



# Add database migration function to the app instance for easy access

@app.on_event("startup")
async def run_migrations():
    """
    Runs database migrations using Alembic on startup.
    """
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")

# Root and health check endpoints
@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.PROJECT_NAME} API", "version": __version__}

@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify the API is operational.
    """
    return {"status": "healthy", "version": __version__}

# Middleware to log execution time of each request
@app.middleware("http")
async def log_request_time(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    logger.info(f"Processed {request.method} {request.url.path} in {process_time} seconds")
    return response

