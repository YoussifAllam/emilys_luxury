import base64
import requests
from rest_framework import status
from rest_framework.response import Response
from django.conf import settings
import logging
import uuid
logger = logging.getLogger(__name__)
from ..models import Payment
from apps.orders.models import Order as oreder_model
from . import investor_balance_tasks
from ..db_services import selectors #, services



def create_moyasar_payment(request_data, validated_data, Target_order: oreder_model):
    api_key = settings.SECRET_KEY
    encoded_api_key = base64.b64encode(api_key.encode()).decode()
    headers = {
        'Authorization': f'Basic {encoded_api_key}',
        'Content-Type': 'application/json',
    }
    
    source_type = request_data['source']['type']
    
    if source_type == 'creditcard':
        source = {
            'type': 'creditcard',
            'name': request_data['source']['name'],
            'number': request_data['source']['number'],
            'cvc': request_data['source']['cvc'],
            'month': request_data['source']['month'],
            'year': request_data['source']['year']
        }
    elif source_type == 'stcpay':
        source = {
            'type': 'stcpay',
            'mobile': request_data['source']['mobile']
        }
    elif source_type == 'applepay':
        source = {
            'type': 'applepay',
            'token': request_data['source']['token']
        }
    else:
        return None, Response({"error": "Unsupported payment type"}, status=status.HTTP_400_BAD_REQUEST)
    
    payload = {
        'amount': int(Target_order.total_price * 100),  # Convert to halalas
        'currency': 'SAR',
        'description': 'Test description',  # Todo
        'source': source,
        'callback_url': settings.CALLBACKURL,
    }
    
    response = requests.post('https://api.moyasar.com/v1/payments', json=payload, headers=headers)
    
    if response.status_code == 201:
        payment_response = response.json()
        payment_id = payment_response['id']
        
        # Store payment information
        payment = Payment.objects.create(
            id=payment_id,
            order_uuid=Target_order.uuid,
            amount=Target_order.total_price,
            status='pending'
        )
        
        return payment_id, str(Target_order.uuid), response
    
    return None, None, response

def process_callback(request):
    payment_data = request.data if request.method == 'POST' else request.query_params
    logger.info(f"Callback received: {payment_data}")

    payment_id = payment_data.get('id')
    payment_status = payment_data.get('status', 'unpaid')

    # Log the received payment_id and status
    logger.info(f"Received payment_id: {payment_id}, payment_status: {payment_status}")

    # Validate the payment_id format
    try:
        payment_uuid = uuid.UUID(payment_id)
    except ValueError:
        logger.error(f"Invalid payment_id format: {payment_id}")
        return Response({"error": "Invalid payment_id format."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        payment = Payment.objects.get(id=payment_uuid)
        payment.status = payment_status
        payment.save()
        
        # Retrieve the order using the stored order_uuid
        order_uuid = payment.order_uuid
        Target_order = selectors.get_order_by_uuid(order_uuid)
        investor_balance_tasks.update_investor_balance(Target_order)

        logger.info(f"Payment status updated: {payment.id} -> {payment.status}")
        return Response({"message": "Payment status updated successfully."}, status=status.HTTP_200_OK)
    except Payment.DoesNotExist:
        logger.error(f"Payment not found for ID: {payment_id}")
        return Response({"error": "Payment not found."}, status=status.HTTP_404_NOT_FOUND)






"""
# def create_moyasar_payment(request_data, validated_data , Target_order: oreder_model):
#     # print('order_price' , Target_order.total_price , "   " , type(Target_order.total_price))
#     api_key = settings.SECRET_KEY
#     encoded_api_key = base64.b64encode(api_key.encode()).decode()
#     headers = {
#             'Authorization': f'Basic {encoded_api_key}',
#             'Content-Type': 'application/json',
#         }
        
#     source_type = request_data['source']['type']
    
#     if source_type == 'creditcard':
#         source = {
#             'type': 'creditcard',
#             'name': request_data['source']['name'],
#             'number': request_data['source']['number'],
#             'cvc': request_data['source']['cvc'],
#             'month': request_data['source']['month'],
#             'year': request_data['source']['year']
#         }
#     elif source_type == 'stcpay':
#         source = {
#             'type': 'stcpay',
#             'mobile': request_data['source']['mobile']
#         }
#     elif source_type == 'applepay':
#         source = {
#             'type': 'applepay',
#             'token': request_data['source']['token']
#         }
#     else:
#         return None, Response({"error": "Unsupported payment type"}, status=status.HTTP_400_BAD_REQUEST)
    
#     payload = {
#         'amount': int(Target_order.total_price * 100),  # Convert to halalas
#         'currency': 'SAR',
#         'description': 'Test description',  # Todo
#         'source': source,
#         'callback_url': settings.CALLBACKURL,
#         # 'metadata': {
#         #     'order_uuid': Target_order.uuid  # Include order_uuid in metadata
#         # }
#     }
    
#     # print('Payload:', payload)
    
#     response = requests.post('https://api.moyasar.com/v1/payments', json=payload, headers=headers)
    
#     if response.status_code == 201:
#         payment_response = response.json()
#         return payment_response['id'], response 
    
#     return None, response , None



# def process_callback(request):
#         payment_data = request.data if request.method == 'POST' else request.query_params
#         logger.info(f"Callback received: {payment_data}")

#         # print(payment_data.get('metadata') , '++++++++++++++++++++++++')
#         # order_uuid = payment_data.get('metadata', {}).get('order_uuid')
#         # if not order_uuid:
#         #     logger.error("order_uuid not found in callback data")
#         #     return Response({"error": "order_uuid not found in callback data"}, status=status.HTTP_400_BAD_REQUEST)

#         # Target_order = selectors.get_order_by_uuid(order_uuid)
#         # investor_balance_tasks.update_investor_balance(Target_order)

#         payment_id = payment_data.get('id')
#         payment_status = 'paid'

#         # Log the received payment_id and status
#         logger.info(f"Received payment_id: {payment_id}, payment_status: {payment_status}")

#         # Validate the payment_id format
#         try:
#             payment_uuid = uuid.UUID(payment_id)
#         except ValueError:
#             logger.error(f"Invalid payment_id format: {payment_id}")
#             return Response({"error": "Invalid payment_id format."}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             payment = Payment.objects.get(id=payment_uuid)
#             payment.status = payment_status
#             payment.save()
#             logger.info(f"Payment status updated: {payment.id} -> {payment.status}")
#             return Response({"message": "Payment status updated successfully."}, status=status.HTTP_200_OK)
#         except Payment.DoesNotExist:
#             logger.error(f"Payment not found for ID: {payment_id}")
#             return Response({"error": "Payment not found."}, status=status.HTTP_404_NOT_FOUND)
        
# 
"""