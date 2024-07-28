"""
This module initializes the endpoints package and provides utilities for endpoint management.
"""

import logging
import inspect
from fastapi import APIRouter, FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from .lock_card import router as lock_card_router
from .transactions import router as transactions_router

# Initialize logger
logger = logging.getLogger(__name__)

# Create a main router to aggregate all endpoints
api_router = APIRouter()

# Automatically register all routers from submodules
for _, module in inspect.getmembers(inspect.getmodule(api_router), inspect.ismodule):
    for _, obj in inspect.getmembers(module, inspect.isclass):
        if isinstance(obj, APIRouter):
            api_router.include_router(obj)
            logger.info(f"Registered router: {obj}")

# Versioning
api_router.prefix = "/v1"  # Add API version prefix
logger.info("API versioning enabled: /v1")

# Rate Limiting (Placeholder, needs implementation)
# ... (e.g., using slowapi, fastapi-limiter)

# Authentication Middleware (Placeholder, needs implementation)
# ... (e.g., using fastapi-users, OAuth2, JWT)

# Logging Middleware
@api_router.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response: {response.status_code}")
    return response

# CORS Middleware
origins = ["*"]  # Replace with allowed origins in production
api_router.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Error Handling Middleware
@api_router.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()},
    )

# Health Check Endpoint
@api_router.get("/health")
async def health_check():
    return {"status": "ok"}

# Version of the endpoints package
__version__ = "0.1.1"

# Endpoint metadata
# ... (unchanged from the original)

# TODO:
# 1. Implement rate limiting using a suitable library (e.g., slowapi, fastapi-limiter)
# 2. Add authentication middleware (e.g., fastapi-users, OAuth2, JWT)
# 3. Create a system for API documentation generation (e.g., using FastAPI's built-in docs or Swagger UI)
# 4. Implement more comprehensive error handling for specific exception types
# 5. Implement request validation using Pydantic models within the endpoint functions
# 6. Create unit tests for each endpoint to ensure correctness and reliability
