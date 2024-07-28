from datetime import datetime, timedelta
from typing import List, Dict
from pydantic import BaseModel
from collections import defaultdict

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

class Budget(BaseModel):
    category: str
    amount: float

class FinancialData(BaseModel):
    user_id: str
    transactions: List[Transaction]
    accounts: List[Account]
    budgets: List[Budget]
    credit_score: int = None
    last_updated: datetime

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

class FinancialAgent:
    def analyze_financial_data(self, data: FinancialData) -> FinancialReport:
        total_income = sum(t.amount for t in data.transactions if t.amount > 0)
        total_expenses = sum(t.amount for t in data.transactions if t.amount < 0)
        net_savings = total_income + total_expenses  # expenses are negative

        expense_breakdown = defaultdict(float)
        for t in data.transactions:
            if t.amount < 0:
                expense_breakdown[t.category] += abs(t.amount)

        top_spending_categories = sorted(expense_breakdown, key=expense_breakdown.get, reverse=True)[:3]

        account_balances = {account.name: account.balance for account in data.accounts}

        monthly_reports = self.generate_monthly_reports(data.transactions)

        budget_comparisons = self.compare_budget_to_actual(data.budgets, expense_breakdown)

        return FinancialReport(
            user_id=data.user_id,
            total_income=total_income,
            total_expenses=abs(total_expenses),
            net_savings=net_savings,
            expense_breakdown=dict(expense_breakdown),
            top_spending_categories=top_spending_categories,
            account_balances=account_balances,
            credit_score=data.credit_score or 0,
            report_date=datetime.now(),
            monthly_reports=monthly_reports,
            budget_comparisons=budget_comparisons
        )

    def generate_monthly_reports(self, transactions: List[Transaction]) -> List[MonthlyReport]:
        monthly_data = defaultdict(lambda: {'income': 0, 'expenses': defaultdict(float)})
        
        for t in transactions:
            month = t.date.strftime('%Y-%m')
            if t.amount > 0:
                monthly_data[month]['income'] += t.amount
            else:
                monthly_data[month]['expenses'][t.category] += abs(t.amount)

        monthly_reports = []
        for month, data in monthly_data.items():
            total_expenses = sum(data['expenses'].values())
            monthly_reports.append(MonthlyReport(
                month=month,
                total_income=data['income'],
                total_expenses=total_expenses,
                net_savings=data['income'] - total_expenses,
                expense_breakdown=dict(data['expenses'])
            ))

        return sorted(monthly_reports, key=lambda x: x.month)

    def compare_budget_to_actual(self, budgets: List[Budget], actual_expenses: Dict[str, float]) -> List[BudgetComparison]:
        comparisons = []
        for budget in budgets:
            actual = actual_expenses.get(budget.category, 0)
            difference = budget.amount - actual
            comparisons.append(BudgetComparison(
                category=budget.category,
                budgeted=budget.amount,
                actual=actual,
                difference=difference
            ))
        return comparisons

    def generate_advice(self, report: FinancialReport) -> List[str]:
        advice = []
        
        # Credit score advice
        if report.credit_score < 600:
            advice.append("Your credit score is poor. You suck right now lol. Focus on paying bills on time and reducing credit card balances.")
        elif report.credit_score < 700:
            advice.append("Your credit score could be improved. Continue to pay bills on time and reduce credit utilization.")
        elif report.credit_score >= 700:
            advice.append("Great job on maintaining a good credit score! Keep up the good work, dont drop the ball on bills.")

        # Savings rate advice
        savings_rate = (report.net_savings / report.total_income) * 100 if report.total_income > 0 else 0
        if savings_rate < 10:
            advice.append(f"Your savings rate is low at {savings_rate:.1f}%. Try to save at least 10% of your income.")
        elif savings_rate < 20:
            advice.append(f"Your savings rate of {savings_rate:.1f}% is good. Aim to increase it to 20% for better financial security.")
        else:
            advice.append(f"Excellent savings rate of {savings_rate:.1f}%! You're on track for a strong financial future.")

        # Expense category advice
        if report.top_spending_categories:
            top_category = report.top_spending_categories[0]
            category_expense = report.expense_breakdown[top_category]
            category_percentage = (category_expense / report.total_expenses) * 100 if report.total_expenses > 0 else 0
            advice.append(f"Your highest spending category is {top_category}, at {category_percentage:.1f}% of your expenses. Consider if there's room to reduce spending in this area.")

        # Month-to-month comparison advice
        if len(report.monthly_reports) > 1:
            latest_month = report.monthly_reports[-1]
            previous_month = report.monthly_reports[-2]
            income_change = latest_month.total_income - previous_month.total_income
            expense_change = latest_month.total_expenses - previous_month.total_expenses
            
            if income_change > 0:
                advice.append(f"Your income increased by ${income_change:.2f} compared to last month. Great job!")
            elif income_change < 0:
                advice.append(f"Your income decreased by ${abs(income_change):.2f} compared to last month. Consider ways to increase your income.")

            if expense_change > 0:
                advice.append(f"Your expenses increased by ${expense_change:.2f} compared to last month. Try to identify areas where you can cut back.")
            elif expense_change < 0:
                advice.append(f"Your expenses decreased by ${abs(expense_change):.2f} compared to last month. Keep up the good work in managing your spending!")

        # Budget comparison advice
        for comparison in report.budget_comparisons:
            if comparison.difference < 0:
                advice.append(f"You've overspent in the {comparison.category} category by ${abs(comparison.difference):.2f}. Try to cut back on spending in this area.")
            elif comparison.difference > 0:
                advice.append(f"You're under budget in the {comparison.category} category by ${comparison.difference:.2f}. Great job managing your spending!")

        return advice
