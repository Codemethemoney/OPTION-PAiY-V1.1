from typing import Dict, Any
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_alert(alert_type: str, message: str, data: Dict[str, Any] = None):
    """
    Send an alert to the Manager Agent.
    
    :param alert_type: Type of the alert (e.g., 'budget_exceeded', 'unusual_activity')
    :param message: Alert message
    :param data: Additional data related to the alert
    """
    alert = {
        'type': alert_type,
        'message': message,
        'data': data or {}
    }
    
    # Log the alert
    logger.info(f"Alert sent: {alert}")
    
    # TODO: Implement the actual sending mechanism
    # This could involve sending a message to a queue, calling an API, etc.
    # For now, we'll just print it
    print(f"ALERT: {alert_type} - {message}")
    if data:
        print(f"Additional data: {data}")

def budget_exceeded_alert(category: str, amount: float, budget: float):
    """
    Send an alert when a budget category is exceeded.
    
    :param category: Budget category
    :param amount: Actual spent amount
    :param budget: Budget limit
    """
    message = f"Budget exceeded for {category}. Spent ${amount:.2f}, budget was ${budget:.2f}"
    send_alert('budget_exceeded', message, {'category': category, 'amount': amount, 'budget': budget})

def unusual_activity_alert(transaction_id: str, amount: float, reason: str):
    """
    Send an alert for unusual account activity.
    
    :param transaction_id: ID of the unusual transaction
    :param amount: Transaction amount
    :param reason: Reason for flagging the transaction as unusual
    """
    message = f"Unusual activity detected. Transaction ID: {transaction_id}, Amount: ${amount:.2f}"
    send_alert('unusual_activity', message, {'transaction_id': transaction_id, 'amount': amount, 'reason': reason})

def low_balance_alert(account_id: str, balance: float, threshold: float):
    """
    Send an alert when an account balance falls below a certain threshold.
    
    :param account_id: ID of the account
    :param balance: Current balance
    :param threshold: Balance threshold for the alert
    """
    message = f"Low balance alert for account {account_id}. Current balance: ${balance:.2f}, Threshold: ${threshold:.2f}"
    send_alert('low_balance', message, {'account_id': account_id, 'balance': balance, 'threshold': threshold})
