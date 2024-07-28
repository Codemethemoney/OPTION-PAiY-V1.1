#!/bin/bash

# Test the root endpoint
echo "Testing root endpoint:"
curl -X GET http://127.0.0.1:8000/

echo -e "\n\nTesting analyze_finances endpoint:"
curl -X POST http://127.0.0.1:8000/analyze_finances \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test_user",
    "transactions": [
      {
        "id": "1",
        "amount": 1000,
        "description": "Salary",
        "category": "Income",
        "date": "2023-07-01T00:00:00"
      },
      {
        "id": "2",
        "amount": -500,
        "description": "Rent",
        "category": "Housing",
        "date": "2023-07-05T00:00:00"
      }
    ],
    "accounts": [
      {
        "id": "1",
        "name": "Checking",
        "balance": 1500,
        "type": "Checking"
      }
    ],
    "credit_score": 720,
    "last_updated": "2023-07-10T00:00:00"
  }'

echo -e "\n\nTesting bill_reminders endpoint:"
curl -X GET http://127.0.0.1:8000/bill_reminders
