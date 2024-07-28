from typing import Dict, Any, Tuple
import re
from datetime import datetime, timedelta

def parse_sms_command(sms_text: str) -> Tuple[str, Dict[str, Any]]:
    """
    Parse an SMS command and extract the command type and parameters.
    
    :param sms_text: The full text of the SMS message
    :return: A tuple containing the command type and a dictionary of parameters
    """
    words = sms_text.lower().split()
    if not words:
        raise ValueError("Empty SMS command")

    command = words[0]
    params = {}

    if command == "balance":
        if len(words) > 1:
            params["account"] = " ".join(words[1:])
    elif command == "spend":
        if len(words) >= 4:
            params["amount"] = words[1]
            params["category"] = words[2]
            params["description"] = " ".join(words[3:])
    elif command == "transfer":
        if len(words) >= 4:
            params["amount"] = words[1]
            params["from_account"] = words[2]
            params["to_account"] = words[3]
    elif command == "budget":
        if len(words) > 1:
            params["category"] = " ".join(words[1:])
    elif command in ["yes", "no"]:
        params["response"] = command
        if len(words) > 1:
            params["bill_id"] = words[1]
    else:
        raise ValueError(f"Unknown command: {command}")

    return command, params

def execute_sms_command(command: str, params: Dict[str, Any]) -> str:
    """
    Execute an SMS command and return a response.
    
    :param command: The type of command to execute
    :param params: A dictionary of parameters for the command
    :return: A string response to be sent back to the user
    """
    if command == "balance":
        return get_balance(params.get("account"))
    elif command == "spend":
        return record_spending(params["amount"], params["category"], params["description"])
    elif command == "transfer":
        return transfer_money(params["amount"], params["from_account"], params["to_account"])
    elif command == "budget":
        return get_budget_info(params["category"])
    elif command in ["yes", "no"]:
        return handle_bill_payment_response(command, params.get("bill_id"))
    else:
        raise ValueError(f"Unknown command: {command}")

def get_balance(account: str = None) -> str:
    # TODO: Implement actual balance retrieval logic
    if account:
        return f"Your balance for {account} is $1000.00"
    else:
        return "Your total balance is $5000.00"

def record_spending(amount: str, category: str, description: str) -> str:
    # TODO: Implement actual spending record logic
    return f"Recorded spending of ${amount} for {category}: {description}"

def transfer_money(amount: str, from_account: str, to_account: str) -> str:
    # TODO: Implement actual money transfer logic
    return f"Transferred ${amount} from {from_account} to {to_account}"

def get_budget_info(category: str) -> str:
    # TODO: Implement actual budget retrieval logic
    return f"Your budget for {category} is $500.00, you've spent $300.00 so far this month"

def handle_bill_payment_response(response: str, bill_id: str) -> str:
    if response == "yes":
        return pay_bill(bill_id)
    elif response == "no":
        return reschedule_bill_reminder(bill_id)
    else:
        return "Invalid response. Please reply with 'YES' or 'NO'."

def pay_bill(bill_id: str) -> str:
    # TODO: Implement actual bill payment logic with LangChain Agent
    return f"Bill {bill_id} has been paid successfully."

def reschedule_bill_reminder(bill_id: str) -> str:
    # TODO: Implement actual rescheduling logic with LangChain Agent
    new_reminder_date = datetime.now() + timedelta(days=3)
    return f"Bill reminder for bill {bill_id} has been rescheduled for {new_reminder_date.strftime('%Y-%m-%d')}."

def send_bill_reminder(bill_id: str, amount: float, due_date: str) -> str:
    """
    Generate a bill reminder message to be sent to the user.
    
    :param bill_id: The ID of the bill
    :param amount: The amount due
    :param due_date: The due date of the bill
    :return: A string message to be sent to the user
    """
    return f"You have a bill (ID: {bill_id}) of ${amount:.2f} due on {due_date}. Would you like to pay it now? Reply 'YES {bill_id}' to pay or 'NO {bill_id}' to remind you later."

# Example usage
if __name__ == "__main__":
    sample_sms = "spend 50.00 groceries weekly shopping"
    command, params = parse_sms_command(sample_sms)
    response = execute_sms_command(command, params)
    print(response)

    # Example of bill reminder and response
    print(send_bill_reminder("BILL123", 100.50, "2023-07-30"))
    
    sample_response = "yes BILL123"
    command, params = parse_sms_command(sample_response)
    response = execute_sms_command(command, params)
    print(response)

    sample_response = "no BILL123"
    command, params = parse_sms_command(sample_response)
    response = execute_sms_command(command, params)
    print(response)
