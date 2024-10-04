import base64
import requests
from django.conf import settings
from uuid import uuid4
from apps.orders.models import Order as order_models


def update_order_status_to_cancel_after_refund(
    target_order: order_models,
) -> tuple[dict, int]:
    target_order.status = "cancelled"
    target_order.save()


def refund_moyasar_order(
    payment_id: uuid4, amount: int, order_id: uuid4, target_order: order_models
) -> tuple[dict, int]:
    api_key = settings.SECRET_KEY
    encoded_api_key = base64.b64encode(api_key.encode()).decode()

    headers = {
        "Authorization": f"Basic {encoded_api_key}",
        "Content-Type": "application/json",
    }
    # print(amount , "5"*50 ,type(amount))

    payload = {
        "amount": amount * 100,
        "currency": "SAR",
        "description": f"Refund for order ID: {order_id}",
    }

    refund_url = f"https://api.moyasar.com/v1/payments/{payment_id}/refund"

    with requests.Session() as session:
        response = session.post(refund_url, json=payload, headers=headers)

    if response.status_code == 200:
        update_order_status_to_cancel_after_refund(target_order)

    return response.json(), response.status_code
