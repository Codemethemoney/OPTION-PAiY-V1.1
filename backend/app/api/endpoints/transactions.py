"""
This module implements the API endpoints for handling user transactions.
"""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime

from app.api.dependencies import get_current_user, get_transaction_service
from app.services.transaction_service import (
    TransactionService, TransactionCreate, TransactionUpdate, TransactionNotFoundError
)
from app.models.transaction import Transaction
from app.utils.rate_limit import rate_limit

router = APIRouter()

# ... (TransactionBase, CreateTransactionRequest, TransactionResponse models are the same)

@router.post("/transactions", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
@rate_limit(limit=10, period=60)  # 10 requests per minute (adjustable)
async def create_transaction(
    transaction: CreateTransactionRequest,
    current_user: Dict = Depends(get_current_user),
    transaction_service: TransactionService = Depends(get_transaction_service)
) -> TransactionResponse:
    """Create a new transaction for the current user."""
    try:
        new_transaction = transaction_service.create_transaction(
            TransactionCreate(user_id=current_user["id"], **transaction.dict())
        )
        return TransactionResponse.from_orm(new_transaction)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create transaction: {str(e)}"
        )

@router.get("/transactions", response_model=List[TransactionResponse])
async def get_transactions(
    start_date: Optional[datetime] = Query(None, description="Start date for transaction query"),
    end_date: Optional[datetime] = Query(None, description="End date for transaction query"),
    category: Optional[str] = Query(None, description="Filter transactions by category"),
    min_amount: Optional[float] = Query(None, description="Filter transactions by minimum amount"),
    max_amount: Optional[float] = Query(None, description="Filter transactions by maximum amount"),
    limit: int = Query(50, le=100, description="Number of transactions to return (max 100)"),
    offset: int = Query(0, ge=0, description="Number of transactions to skip"),
    current_user: Dict = Depends(get_current_user),
    transaction_service: TransactionService = Depends(get_transaction_service)
) -> List[TransactionResponse]:
    """Retrieve a list of transactions for the current user with filtering and pagination."""

    transactions = transaction_service.get_transactions(
        user_id=current_user["id"],
        start_date=start_date,
        end_date=end_date,
        category=category,
        min_amount=min_amount,
        max_amount=max_amount,
        limit=limit,
        offset=offset
    )
    return [TransactionResponse.from_orm(t) for t in transactions]

# ... (get_transaction endpoint is the same)

@router.put("/transactions/{transaction_id}", response_model=TransactionResponse)
async def update_transaction(
    transaction_id: str,
    transaction_data: TransactionBase,
    current_user: Dict = Depends(get_current_user),
    transaction_service: TransactionService = Depends(get_transaction_service),
) -> TransactionResponse:
    """Update an existing transaction."""
    try:
        updated_transaction = transaction_service.update_transaction(
            current_user["id"], transaction_id, TransactionUpdate(**transaction_data.dict())
        )
        return TransactionResponse.from_orm(updated_transaction)
    except TransactionNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to update transaction: {str(e)}")


@router.delete("/transactions/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(
    transaction_id: str,
    current_user: Dict = Depends(get_current_user),
    transaction_service: TransactionService = Depends(get_transaction_service),
):
    """Delete a transaction."""
    try:
        transaction_service.delete_transaction(current_user["id"], transaction_id)
        return {"message": "Transaction deleted successfully"}
    except TransactionNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete transaction: {str(e)}"
        )
