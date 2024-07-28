from typing import Dict, Any, List
from pydantic import ValidationError
from app.models.financial_data import FinancialData, Transaction, Account, User
from app.models.financial_report import FinancialReport, FinancialAdvice

class PydanticAgent:
    @staticmethod
    def validate_financial_data(data: Dict[str, Any]) -> FinancialData:
        try:
            return FinancialData(**data)
        except ValidationError as e:
            raise ValueError(f"Invalid financial data: {e}")

    @staticmethod
    def validate_transaction(data: Dict[str, Any]) -> Transaction:
        try:
            return Transaction(**data)
        except ValidationError as e:
            raise ValueError(f"Invalid transaction data: {e}")

    @staticmethod
    def validate_account(data: Dict[str, Any]) -> Account:
        try:
            return Account(**data)
        except ValidationError as e:
            raise ValueError(f"Invalid account data: {e}")

    @staticmethod
    def validate_user(data: Dict[str, Any]) -> User:
        try:
            return User(**data)
        except ValidationError as e:
            raise ValueError(f"Invalid user data: {e}")

    @staticmethod
    def validate_financial_report(data: Dict[str, Any]) -> FinancialReport:
        try:
            return FinancialReport(**data)
        except ValidationError as e:
            raise ValueError(f"Invalid financial report: {e}")

    @staticmethod
    def validate_financial_advice(data: Dict[str, Any]) -> FinancialAdvice:
        try:
            return FinancialAdvice(**data)
        except ValidationError as e:
            raise ValueError(f"Invalid financial advice: {e}")

    @staticmethod
    def sanitize_input(input_data: Dict[str, Any]) -> Dict[str, Any]:
        sanitized_data = {}
        for key, value in input_data.items():
            if isinstance(value, str):
                # Remove any potentially harmful characters
                sanitized_data[key] = ''.join(char for char in value if char.isalnum() or char in [' ', '-', '_', '.', '@'])
            elif isinstance(value, (int, float, bool)):
                sanitized_data[key] = value
            elif isinstance(value, list):
                sanitized_data[key] = [PydanticAgent.sanitize_input(item) if isinstance(item, dict) else item for item in value]
            elif isinstance(value, dict):
                sanitized_data[key] = PydanticAgent.sanitize_input(value)
            else:
                sanitized_data[key] = str(value)
        return sanitized_data

    @classmethod
    def validate_and_sanitize_financial_data(cls, data: Dict[str, Any]) -> FinancialData:
        sanitized_data = cls.sanitize_input(data)
        return cls.validate_financial_data(sanitized_data)

    @classmethod
    def bulk_validate_transactions(cls, transactions: List[Dict[str, Any]]) -> List[Transaction]:
        valid_transactions = []
        errors = []
        for i, transaction_data in enumerate(transactions):
            try:
                valid_transaction = cls.validate_transaction(transaction_data)
                valid_transactions.append(valid_transaction)
            except ValueError as e:
                errors.append(f"Error in transaction {i}: {str(e)}")
        
        if errors:
            raise ValueError(f"Errors in bulk transaction validation: {'; '.join(errors)}")
        
        return valid_transactions
