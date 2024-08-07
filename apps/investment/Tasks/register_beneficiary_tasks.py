import base64
import requests
from django.conf import settings
import logging
logger = logging.getLogger(__name__)
import json

def register_beneficiary_account(data: json):
    api_key = settings.SECRET_KEY
    encoded_api_key = base64.b64encode(api_key.encode()).decode()
    headers = {
        'Authorization': f'Basic {encoded_api_key}',
        'Content-Type': 'application/json',
    }

    payload = {
        'name': data['account_owner_name'],
        'number': data['credit_card_number'],
        'bank_name': data['bank_name'],
        'type': 'creditcard',
        "account_type": "bank",
        "properties": {
            "iban": data['iban']
        },
        "credentials": {
            "client_id": settings.PUBLISHABLE_KEY,
            "client_secret": settings.SECRET_KEY ,
            
            # Todo----------
            "company_code": "a3847358-0442-4a4b-88e1-1bb96c960933",  # Use the actual company code obtained
            "cert": "your_actual_cert_value",  # Use the actual certificate value obtained
            "key": "your_actual_key_value" 
        }
    }

    response = requests.post('https://api.moyasar.com/v1/payout_accounts', json=payload, headers=headers)

    if response.status_code == 201:
        return response.json(), response.json()  # Return the registered account details
    else:
        logger.error(f"Failed to register beneficiary account: {response.json()}")
        print('++++++++++++++++', response.json())
        return response.json(), None



def Create_Wallet(data: json):
    api_key = settings.SECRET_KEY
    encoded_api_key = base64.b64encode(api_key.encode()).decode()
    headers = {
        'Authorization': f'Basic {encoded_api_key}',
        'Content-Type': 'application/json',
    }

    payload =  {
            "account_type": "bank",
            "properties": {
                "type": "stcpay",
                'iban': data['iban'],
                
            }
            ,"credentials": {
            "client_id": settings.PUBLISHABLE_KEY,
            "client_secret": settings.SECRET_KEY ,
            }
            
                }
    

    response = requests.post('https://api.moyasar.com/v1/payout_accounts', json=payload, headers=headers)

    if response.status_code == 201:
        return response.json(), response.json()  # Return the registered account details
    else:
        logger.error(f"Failed to register beneficiary account: {response.json()}")
        # print('++++++++++++++++', response.json())
        return response.json(), None