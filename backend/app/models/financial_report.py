from pydantic import BaseModel
from typing import List, Dict
from datetime import datetime

class MonthlyReport(BaseModel):
    month: str
    total_income: float
    total_expenses: float
    net_savings: float
    expense_breakdown: Dict[str, float]

class BudgetComparison(BaseModel):
    category: str
    budgeted: float
    actual: float
    difference: float

class FinancialReport(BaseModel):
    user_id: str
    total_income: float
    total_expenses: float
    net_savings: float
    expense_breakdown: Dict[str, float]
    top_spending_categories: List[str]
    account_balances: Dict[str, float]
    credit_score: int
    report_date: datetime
    monthly_reports: List[MonthlyReport]
    budget_comparisons: List[BudgetComparison]

class FinancialAdvice(BaseModel):
    category: str
    advice: str
    potential_savings: float

class ComprehensiveFinancialReport(FinancialReport):
    advice: List[FinancialAdvice]
