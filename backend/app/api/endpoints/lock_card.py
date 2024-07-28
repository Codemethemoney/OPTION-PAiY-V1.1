"""
This module implements the API endpoint for locking and unlocking the user's card.
"""
import logging
from fastapi import APIRouter, Depends, HTTPException, status, Request
from pydantic import BaseModel, Field
from typing import Dict, Optional
from datetime import datetime, timedelta

from app.api.dependencies import get_current_user, get_card_service
from app.services.card_service import CardService, CardLockError, CardNotFoundError
from app.models.card import Card
from app.utils.rate_limit import SlidingWindowRateLimiter
from app.utils.audit_log import log_card_action

router = APIRouter()
logger = logging.getLogger(__name__)

class LockCardRequest(BaseModel):
    reason: str = Field(..., description="Reason for locking the card", max_length=255)
    card_id: Optional[int] = Field(None, description="ID of the card to lock (optional for single card users)")

class LockCardResponse(BaseModel):
    status: str
    message: str

# Initialize rate limiter (adjust parameters as needed)
rate_limiter = SlidingWindowRateLimiter(limit=5, period=60)  # 5 requests per minute

@router.post("/card/lock", response_model=LockCardResponse)
async def lock_card(request: LockCardRequest, current_user: Dict = Depends(get_current_user),
                   card_service: CardService = Depends(get_card_service)) -> LockCardResponse:
    """Lock the user's card."""
    if not rate_limiter.allow_request(current_user["id"]):
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Rate limit exceeded")

    try:
        card = card_service.lock_card(current_user["id"], request.reason, request.card_id)
        log_card_action(current_user["id"], card.id, "lock", request.reason)
        return LockCardResponse(status="success", message="Card has been successfully locked.")
    except CardNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Card not found")
    except CardLockError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/card/lock", response_model=LockCardResponse)
async def unlock_card(request: Request, current_user: Dict = Depends(get_current_user),
                     card_service: CardService = Depends(get_card_service)) -> LockCardResponse:
    """Unlock the user's card."""
    if not rate_limiter.allow_request(current_user["id"]):
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Rate limit exceeded")

    try:
        card = card_service.unlock_card(current_user["id"], request.query_params.get('card_id'))
        log_card_action(current_user["id"], card.id, "unlock")
        return LockCardResponse(status="success", message="Card has been successfully unlocked.")
    except CardNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Card not found")
    except CardLockError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/card/lock/status", response_model=Dict[str, bool])
async def get_card_lock_status(
    current_user: Dict = Depends(get_current_user),
    card_service: CardService = Depends(get_card_service),
    card_id: Optional[int] = None,
) -> Dict[str, bool]:
    """Get the current lock status of the user's card."""

    try:
        is_locked = card_service.get_card_lock_status(current_user["id"], card_id)
        return {"is_locked": is_locked}
    except CardNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Card not found")
    except Exception as e:
        logger.error(f"Failed to retrieve card lock status: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Failed to retrieve card lock status")

