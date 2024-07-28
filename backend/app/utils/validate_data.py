from pydantic import ValidationError
from app.models.financial_data import FinancialData
from app.models.financial_report import FinancialReport

def validate_financial_data(data: dict) -> FinancialData:
    try:
        return FinancialData(**data)
    except ValidationError as e:
        raise ValueError(f"Invalid financial data: {e}")

def validate_financial_report(data: dict) -> FinancialReport:
    try:
        return FinancialReport(**data)
    except ValidationError as e:
        raise ValueError(f"Invalid financial report: {e}")

def sanitize_input(input_data: dict) -> dict:
    # Implement input sanitization logic here
    # For example, remove any potentially harmful characters or scripts
    sanitized_data = {}
    for key, value in input_data.items():
        if isinstance(value, str):
            # Remove any potentially harmful characters
            sanitized_data[key] = ''.join(char for char in value if char.isalnum() or char in [' ', '-', '_', '.', '@'])
        else:
            sanitized_data[key] = value
    return sanitized_data

def validate_and_sanitize_financial_data(data: dict) -> FinancialData:
    sanitized_data = sanitize_input(data)
    return validate_financial_data(sanitized_data)
