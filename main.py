from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from database import SessionLocal, engine, User, Transaction, Account, BillReminder, Budget
from agents.financial_agent import FinancialAgent, FinancialData, FinancialReport

app = FastAPI()
financial_agent = FinancialAgent()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class UserCreate(BaseModel):
    username: str
    password: str

class TransactionCreate(BaseModel):
    amount: float
    description: str
    category: str
    date: datetime

class AccountCreate(BaseModel):
    name: str
    balance: float
    type: str

class BillReminderCreate(BaseModel):
    description: str
    amount: float
    due_date: datetime

class CreditScoreUpdate(BaseModel):
    credit_score: int

class BudgetCreate(BaseModel):
    category: str
    amount: float

@app.get("/")
def read_root():
    return {"message": "Welcome to the Financial API"}

@app.post("/users/", response_model=dict)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(username=user.username, hashed_password=user.password)  # In real app, hash the password
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"id": db_user.id, "username": db_user.username}

@app.post("/transactions/", response_model=dict)
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    db_transaction = Transaction(**transaction.dict(), user_id=1)  # Hardcoded user_id for simplicity
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return {"id": db_transaction.id, "description": db_transaction.description}

@app.post("/accounts/", response_model=dict)
def create_account(account: AccountCreate, db: Session = Depends(get_db)):
    db_account = Account(**account.dict(), user_id=1)  # Hardcoded user_id for simplicity
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return {"id": db_account.id, "name": db_account.name}

@app.post("/bill_reminders/", response_model=dict)
def create_bill_reminder(bill_reminder: BillReminderCreate, db: Session = Depends(get_db)):
    db_bill_reminder = BillReminder(**bill_reminder.dict(), user_id=1)  # Hardcoded user_id for simplicity
    db.add(db_bill_reminder)
    db.commit()
    db.refresh(db_bill_reminder)
    return {"id": db_bill_reminder.id, "description": db_bill_reminder.description}

@app.get("/bill_reminders/", response_model=List[dict])
def get_bill_reminders(db: Session = Depends(get_db)):
    reminders = db.query(BillReminder).filter(BillReminder.user_id == 1).all()  # Hardcoded user_id for simplicity
    return [{"id": r.id, "description": r.description, "amount": r.amount, "due_date": r.due_date} for r in reminders]

@app.put("/users/{user_id}/credit_score", response_model=dict)
def update_credit_score(user_id: int, credit_score_update: CreditScoreUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.credit_score = credit_score_update.credit_score
    db.commit()
    return {"message": "Credit score updated successfully"}

@app.post("/budgets/", response_model=dict)
def create_budget(budget: BudgetCreate, db: Session = Depends(get_db)):
    db_budget = Budget(**budget.dict(), user_id=1)  # Hardcoded user_id for simplicity
    db.add(db_budget)
    db.commit()
    db.refresh(db_budget)
    return {"id": db_budget.id, "category": db_budget.category, "amount": db_budget.amount}

@app.get("/budgets/", response_model=List[dict])
def get_budgets(db: Session = Depends(get_db)):
    budgets = db.query(Budget).filter(Budget.user_id == 1).all()  # Hardcoded user_id for simplicity
    return [{"id": b.id, "category": b.category, "amount": b.amount} for b in budgets]

@app.get("/analyze_finances/{user_id}", response_model=dict)
def analyze_finances(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    transactions = db.query(Transaction).filter(Transaction.user_id == user_id).all()
    accounts = db.query(Account).filter(Account.user_id == user_id).all()
    budgets = db.query(Budget).filter(Budget.user_id == user_id).all()
    
    financial_data = FinancialData(
        user_id=str(user_id),
        transactions=[
            {
                "id": str(t.id),
                "amount": t.amount,
                "description": t.description,
                "category": t.category,
                "date": t.date
            }
            for t in transactions
        ],
        accounts=[
            {
                "id": str(a.id),
                "name": a.name,
                "balance": a.balance,
                "type": a.type
            }
            for a in accounts
        ],
        budgets=[
            {
                "category": b.category,
                "amount": b.amount
            }
            for b in budgets
        ],
        credit_score=user.credit_score,
        last_updated=datetime.now()
    )
    
    report = financial_agent.analyze_financial_data(financial_data)
    advice = financial_agent.generate_advice(report)
    
    return {"report": report, "advice": advice}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
