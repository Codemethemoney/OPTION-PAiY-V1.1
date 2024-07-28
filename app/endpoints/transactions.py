from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class Transaction(BaseModel):
    id: int
    amount: float
    description: str

# Dummy data for demonstration
transactions = [
    Transaction(id=1, amount=100.0, description="Purchase"),
    Transaction(id=2, amount=-50.0, description="Refund"),
]

@router.get("/transactions", response_model=list[Transaction])
async def get_transactions():
    return transactions

@router.get("/transactions/{transaction_id}", response_model=Transaction)
async def get_transaction(transaction_id: int):
    for transaction in transactions:
        if transaction.id == transaction_id:
            return transaction
    raise HTTPException(status_code=404, detail="Transaction not found")
