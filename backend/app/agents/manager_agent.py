import os
from typing import List, Dict, Any
from app.models.financial_data import FinancialData
from app.models.financial_report import FinancialReport, FinancialAdvice
from app.agents.rag_agent import RAGAgent
from app.agents.langchain_agent import LangChainAgent
from app.agents.pydantic_agent import PydanticAgent
from app.agents.financial_agent import FinancialAgent
from datetime import datetime, timedelta
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class ManagerAgent:
    def __init__(self, financial_agent: FinancialAgent, rag_agent: RAGAgent, langchain_agent: LangChainAgent, pydantic_agent: PydanticAgent):
        self.financial_agent = financial_agent
        self.rag_agent = rag_agent
        self.langchain_agent = langchain_agent
        self.pydantic_agent = pydantic_agent
        
        # Set up OpenAI API key
        openai.api_key = os.getenv('OPENAI_API_KEY')
        if not openai.api_key:
            raise ValueError("No OpenAI API key found in .env file. Please set the OPENAI_API_KEY variable.")

    def process_user_input(self, user_input: str, financial_data: FinancialData, financial_report: FinancialReport) -> str:
        # Use GPT-4 to process user input and determine appropriate action
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a financial assistant. Determine the user's intent from their input."},
                {"role": "user", "content": user_input}
            ]
        )
        intent = response.choices[0].message['content'].strip().lower()

        if "report" in intent:
            return self.generate_report_summary(financial_report)
        elif "advice" in intent:
            return self.get_personalized_advice(financial_data, financial_report)
        elif "question" in intent:
            return self.rag_agent.answer_financial_question(user_input, financial_data, financial_report)
        elif "concept" in intent:
            concept = self.extract_concept(user_input)
            return self.rag_agent.explain_financial_concept(concept)
        else:
            return "I'm sorry, I didn't understand that. Could you please rephrase your question or request?"

    def extract_concept(self, user_input: str) -> str:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Extract the financial concept from the user's input."},
                {"role": "user", "content": user_input}
            ]
        )
        return response.choices[0].message['content'].strip()

    def generate_report_summary(self, financial_report: FinancialReport) -> str:
        report_data = f"""
        Total Income: ${financial_report.total_income:.2f}
        Total Expenses: ${financial_report.total_expenses:.2f}
        Net Savings: ${financial_report.net_savings:.2f}
        Top Spending Categories: {', '.join(financial_report.top_spending_categories)}
        """
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Generate a natural language summary of the following financial report data:"},
                {"role": "user", "content": report_data}
            ]
        )
        return response.choices[0].message['content'].strip()

    def get_personalized_advice(self, financial_data: FinancialData, financial_report: FinancialReport) -> str:
        advice_list = self.rag_agent.generate_personalized_advice(financial_data, financial_report)
        advice_text = "Here are some personalized financial suggestions for you:\n"
        for advice in advice_list:
            advice_text += f"- {advice.advice} This could potentially save you ${advice.potential_savings:.2f}.\n"
        return advice_text

    def check_bill_payments(self, financial_data: FinancialData) -> List[str]:
        # Check for upcoming bills and generate reminders
        reminders = []
        today = datetime.now()
        for transaction in financial_data.transactions:
            if transaction.amount < 0 and transaction.date > today and transaction.date <= today + timedelta(days=7):
                reminders.append(f"Reminder: You have a {transaction.description} payment of ${abs(transaction.amount):.2f} due on {transaction.date.strftime('%Y-%m-%d')}.")
        return reminders

    def process_transaction(self, user_id: str, transaction_data: Dict[str, Any]) -> str:
        try:
            # Validate and sanitize the transaction data
            sanitized_data = self.pydantic_agent.sanitize_input(transaction_data)
            valid_transaction = self.pydantic_agent.validate_transaction(sanitized_data)
            
            # Process the transaction using the LangChain Agent
            created_transaction = self.langchain_agent.create_transaction(
                user_id,
                valid_transaction.amount,
                valid_transaction.description,
                valid_transaction.category
            )
            
            # Check for unusual activity
            if self.langchain_agent.detect_unusual_activity(user_id, created_transaction):
                return f"Transaction processed, but flagged as unusual activity: ${created_transaction.amount:.2f} for {created_transaction.description}"
            
            return f"Transaction processed successfully: ${created_transaction.amount:.2f} for {created_transaction.description}"
        except ValueError as e:
            return f"Error processing transaction: {str(e)}"

    def get_account_summary(self, user_id: str) -> str:
        # Get account summary using the LangChain Agent
        transactions = self.langchain_agent.get_transactions(user_id, start_date=datetime.now() - timedelta(days=30))
        total_income = sum(t.amount for t in transactions if t.amount > 0)
        total_expenses = sum(t.amount for t in transactions if t.amount < 0)
        balance = self.langchain_agent.get_account_balance(user_id, "main_account")  # Assuming a main account
        
        summary = f"Account Summary for the last 30 days:\n"
        summary += f"Total Income: ${total_income:.2f}\n"
        summary += f"Total Expenses: ${abs(total_expenses):.2f}\n"
        summary += f"Net Change: ${(total_income + total_expenses):.2f}\n"
        summary += f"Current Balance: ${balance:.2f}\n"
        
        return summary

    def handle_bill_payment_response(self, user_id: str, bill_id: str, response: str) -> str:
        if response.lower() == "yes":
            if self.langchain_agent.process_bill_payment(user_id, bill_id):
                return f"Bill {bill_id} has been paid successfully."
            else:
                return f"There was an error processing the payment for bill {bill_id}. Please try again later."
        elif response.lower() == "no":
            new_reminder_date = datetime.now() + timedelta(days=3)
            if self.langchain_agent.reschedule_bill_reminder(user_id, bill_id, new_reminder_date):
                return f"The reminder for bill {bill_id} has been rescheduled for {new_reminder_date.strftime('%Y-%m-%d')}."
            else:
                return f"There was an error rescheduling the reminder for bill {bill_id}. Please try again later."
        else:
            return "Invalid response. Please reply with 'YES' to pay the bill or 'NO' to reschedule the reminder."

    # You can add more methods here to utilize the financial_agent if needed
