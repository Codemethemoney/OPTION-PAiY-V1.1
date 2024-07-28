from fastapi import APIRouter
from app.api.endpoints import transactions, bills, user_interaction

api_router = APIRouter()

api_router.include_router(transactions.router, prefix="/transactions", tags=["transactions"])
api_router.include_router(bills.router, prefix="/bills", tags=["bills"])
api_router.include_router(user_interaction.router, prefix="/user", tags=["user"])

# You can add more routers here as you develop more endpoints
