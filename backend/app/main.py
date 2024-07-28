from fastapi import FastAPI, Depends, HTTPException
from app.api.dependencies import get_token_header, get_agents
from app.models.financial_data import FinancialData
from app.models.financial_report import FinancialReport
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI()

class UserInput(BaseModel):
    message: str

class BillReminder(BaseModel):
    reminder: str

@app.post("/process_input")
async def process_input(
    user_input: UserInput,
    agents: Dict = Depends(get_agents),
    token: str = Depends(get_token_header)
):
    manager_agent = agents["manager_agent"]
    # In a real application, you would fetch the user's financial data and report here
    financial_data = FinancialData(user_id="test_user", transactions=[], accounts=[], last_updated=None)
    financial_report = FinancialReport(
        user_id="test_user",
        total_income=0,
        total_expenses=0,
        net_savings=0,
        expense_breakdown=[],
        top_spending_categories=[],
        account_balances={},
        credit_score=0,
        report_date=None
    )
    response = manager_agent.process_user_input(user_input.message, financial_data, financial_report)
    return {"response": response}

@app.get("/bill_reminders")
async def get_bill_reminders(
    agents: Dict = Depends(get_agents),
    token: str = Depends(get_token_header)
):
    manager_agent = agents["manager_agent"]
    # In a real application, you would fetch the user's financial data here
    financial_data = FinancialData(user_id="test_user", transactions=[], accounts=[], last_updated=None)
    reminders = manager_agent.check_bill_payments(financial_data)
    return {"reminders": [BillReminder(reminder=r) for r in reminders]}

@app.get("/periodic_report")
async def get_periodic_report(
    agents: Dict = Depends(get_agents),
    token: str = Depends(get_token_header)
):
    manager_agent = agents["manager_agent"]
    # In a real application, you would fetch the user's financial data here
    financial_data = FinancialData(user_id="test_user", transactions=[], accounts=[], last_updated=None)
    report = manager_agent.generate_periodic_report(financial_data)
    return {"report": report}

@app.on_event("startup")
async def startup_event():
    # This could be used to initialize any resources, like database connections
    pass

@app.on_event("shutdown")
async def shutdown_event():
    # This could be used to clean up any resources
    pass
