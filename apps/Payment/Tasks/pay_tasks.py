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
from . import investor_balance_tasks , order_tasks
from ..db_services import selectors #, services
from .Refund_tasks import refund_moyasar_order

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
        "publishable_api_key": settings.PUBLISHABLE_KEY, 
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

from django.db import transaction

def refund_the_payment(payment_id):
    api_key = settings.SECRET_KEY
    encoded_api_key = base64.b64encode(api_key.encode()).decode()
    refund_response = requests.post(
                    'https://api.moyasar.com/v1/payments/refunds',
                    json={'payment_id': payment_id},
                    headers = {
                        'Authorization': f'Basic {encoded_api_key}',
                        'Content-Type': 'application/json',
    }
                )
    if refund_response.status_code != 200:
        logger.error(f"Failed to refund payment {payment_id} through Moyasar: {refund_response.text}")


def process_callback(request):
    payment_data = request.data if request.method == 'POST' else request.query_params
    logger.info(f"Callback received: {payment_data}")

    payment_id = payment_data.get('id')
    payment_status = payment_data.get('status', 'unpaid')

    logger.info(f"Received payment_id: {payment_id}, payment_status: {payment_status}")

    try:
        payment_uuid = uuid.UUID(payment_id)
    except ValueError:
        logger.error(f"Invalid payment_id format: {payment_id}")
        return Response({"error": "Invalid payment_id format."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        with transaction.atomic():
            payment = Payment.objects.get(id=payment_uuid)
            payment.status = payment_status
            payment.save()

            order_uuid = payment.order_uuid
            Target_order = selectors.get_order_by_uuid(order_uuid)

            # First, handle temporary bookings
            # is_success = order_tasks.confirm_or_cancel_temporary_bookings(Target_order, True)
            is_success = True
            if not is_success:
                logger.error(f"Failed to confirm or cancel temporary bookings for order {order_uuid}. Payment process aborted.")
                # Optionally, mark payment as failed or disputed here
                payment.status = 'failed'
                payment.save()
                # refund_the_payment(payment_id)
                r ,s = refund_moyasar_order(payment_id, int(Target_order.total_price), order_uuid)
                return Response({"error": "Failed to confirm or cancel temporary bookings. Payment process aborted."}, status=status.HTTP_400_BAD_REQUEST)
            
            # Only proceed with payment confirmation if temporary bookings were successfully handled
            if payment_status == 'paid':

                investor_balance_tasks.update_investor_balance(Target_order)
                Target_order.is_payment_completed = True
                Target_order.save()
                logger.info(f"Payment status updated: {payment.id} -> {payment.status}")
                return Response({"message": "Payment status updated successfully."}, status=status.HTTP_200_OK)
            else:
                logger.info(f"Payment failed or not completed: {payment.id} -> {payment.status}")
                return Response({"message": "Payment not completed, booking cancelled."}, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
