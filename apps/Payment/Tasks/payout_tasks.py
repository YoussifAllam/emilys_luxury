# tasks.py
import requests
from django.conf import settings
import base64

def transfer_balance(credit_card_number, amount):
    api_url = "https://api.moyasar.com/v1/transfers"
    api_key = settings.SECRET_KEY
    encoded_api_key = base64.b64encode(api_key.encode()).decode()

    headers = {
        'Authorization': f'Basic {encoded_api_key}',
        'Content-Type': 'application/json'
    }

    payload = {
        "amount": amount * 100,  # Convert to halalas
        "currency": "SAR",
        "source": {
            "type": "creditcard",
            "number": credit_card_number
        },
        "description": "Balance transfer to credit card"
    }

    response = requests.post(api_url, json=payload, headers=headers)

    if response.status_code == 201:
        return {"status": "success", "message": "Balance transferred successfully."}
    else:
        return {"status": "failure", "message": "Balance transfer failed.", "details": response.json()}

def create_moyasar_payout(investor_details, amount):
    api_key = settings.SECRET_KEY
    encoded_api_key = base64.b64encode(api_key.encode()).decode()
    headers = {
        'Authorization': f'Basic {encoded_api_key}',
        'Content-Type': 'application/json',
    }

    payload = {
        'amount': int(amount * 100),  # Convert to halalas
        'currency': 'SAR',
        'description': 'Payout to investor',
        'beneficiary': {
            'type': 'payout_account',
            'id': investor_details.payout_account_id,  # Use the registered account ID
        }
    }
    
    response = requests.post('https://api.moyasar.com/v1/payouts', json=payload, headers=headers)
    
    return response