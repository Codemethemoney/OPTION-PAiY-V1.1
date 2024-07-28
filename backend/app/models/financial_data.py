from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Transaction(BaseModel):
    id: str
    amount: float
    description: str
    category: str
    date: datetime

class Account(BaseModel):
    id: str
    name: str
    balance: float
    type: str

class User(BaseModel):
    id: str
    username: str
    email: str
    credit_score: Optional[int] = None

class FinancialData(BaseModel):
    user_id: str
    transactions: List[Transaction]
    accounts: List[Account]
    credit_score: Optional[int] = None
    last_updated: datetime
