from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.endpoints import transactions

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API for financial management and transactions",
    version="0.1.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(transactions.router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {"message": f"Welcome to the {settings.PROJECT_NAME} API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
