import base64
import requests
from django.conf import settings
from uuid import uuid4
from django.http import HttpResponse

def refund_moyasar_order(payment_id :uuid4 , amount:int , order_id :uuid4) -> HttpResponse:
    api_key = settings.SECRET_KEY  
    encoded_api_key = base64.b64encode(api_key.encode()).decode()
    
    headers = {
        'Authorization': f'Basic {encoded_api_key}',
        'Content-Type': 'application/json',
    }
    
    payload = {
        "amount": amount * 100,  # The amount is usually in the smallest unit (halals)
        "currency": "SAR",
        "description": "Refund for order ID: {}".format(order_id),
    }
    
    refund_url = f'https://api.moyasar.com/v1/payments/{payment_id}/refund'
    
    response = requests.post(refund_url, json=payload, headers=headers)
    
    return response.json() , response.status_code
