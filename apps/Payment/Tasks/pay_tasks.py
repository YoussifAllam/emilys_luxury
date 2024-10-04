import base64
import requests
from rest_framework import status
from rest_framework.response import Response
from django.conf import settings
import logging
import uuid
from ..models import Payment
from apps.orders.models import Order as oreder_model
from . import investor_balance_tasks, order_tasks
from ..db_services import selectors  # , services
from .Refund_tasks import refund_moyasar_order
from django.shortcuts import redirect
from .. import constant
from django.db import transaction

logger = logging.getLogger(__name__)


def create_moyasar_payment(request_data, validated_data, Target_order: oreder_model):
    api_key = settings.SECRET_KEY
    encoded_api_key = base64.b64encode(api_key.encode()).decode()
    headers = {
        "Authorization": f"Basic {encoded_api_key}",
        "Content-Type": "application/json",
    }

    source_type = request_data["source"]["type"]

    if source_type == "creditcard":
        source = {
            "type": "creditcard",
            "name": request_data["source"]["name"],
            "number": request_data["source"]["number"],
            "cvc": request_data["source"]["cvc"],
            "month": request_data["source"]["month"],
            "year": request_data["source"]["year"],
        }
    elif source_type == "stcpay":
        source = {"type": "stcpay", "mobile": request_data["source"]["mobile"]}
    elif source_type == "applepay":
        source = {"type": "applepay", "token": request_data["source"]["token"]}
    else:
        return None, Response(
            {"error": "Unsupported payment type"}, status=status.HTTP_400_BAD_REQUEST
        )

    payload = {
        "publishable_api_key": settings.PUBLISHABLE_KEY,
        "amount": int(Target_order.total_price * 100),  # Convert to halalas
        "currency": "SAR",
        "description": "Test description",  # Todo
        "source": source,
        "callback_url": settings.CALLBACKURL,
    }

    response = requests.post(
        "https://api.moyasar.com/v1/payments", json=payload, headers=headers
    )

    if response.status_code == 201:
        payment_response = response.json()
        payment_id = payment_response["id"]

        # Store payment information
        Payment.objects.create(
            id=payment_id,
            order_uuid=Target_order.uuid,
            amount=Target_order.total_price,
            status="pending",
        )

        return payment_id, str(Target_order.uuid), response

    return None, None, response


def refund_the_payment(payment_id):
    api_key = settings.SECRET_KEY
    encoded_api_key = base64.b64encode(api_key.encode()).decode()
    refund_response = requests.post(
        "https://api.moyasar.com/v1/payments/refunds",
        json={"payment_id": payment_id},
        headers={
            "Authorization": f"Basic {encoded_api_key}",
            "Content-Type": "application/json",
        },
    )
    if refund_response.status_code != 200:
        logger.error(
            f"Failed to refund payment {payment_id} through Moyasar: {refund_response.text}"
        )


def process_callback(request):
    payment_data = request.data if request.method == "POST" else request.query_params
    logger.info(f"Callback received: {payment_data}")

    payment_id = payment_data.get("id")
    payment_status = payment_data.get("status", "unpaid")

    logger.info(f"Received payment_id: {payment_id}, payment_status: {payment_status}")
    print(f"\n Received payment_id: {payment_id}, payment_status: {payment_status}\n")

    if not payment_id:
        logger.error("Missing payment_id in callback data.")
        return Response(
            {"error": "Missing payment_id in callback data."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        payment_uuid = uuid.UUID(payment_id)
    except ValueError:
        logger.error(f"Invalid payment_id format: {payment_id}")
        return Response(
            {"error": "Invalid payment_id format."}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        with transaction.atomic():
            payment = Payment.objects.get(id=payment_uuid)
            payment.status = payment_status
            payment.save()

            order_uuid = payment.order_uuid
            Target_order = selectors.get_order_by_uuid(order_uuid)

            if payment_status == "paid":
                is_success = order_tasks.confirm_or_cancel_temporary_bookings(
                    Target_order, True
                )

                if not is_success:
                    logger.error(
                        f"Failed to confirm or cancel temporary bookings for order {order_uuid}. "
                    )

                    payment.status = "failed"
                    payment.save()
                    r, s = refund_moyasar_order(
                        payment_id, int(Target_order.total_price), order_uuid
                    )
                    # return Response({"error": "Failed to confirm or cancel temporary bookings."},
                    #                 status=status.HTTP_400_BAD_REQUEST)

                    print(f"Payment status updated: {payment.id} -> {payment.status}")
                    return redirect(constant.CALL_BACK_URL)

                investor_balance_tasks.update_investor_balance(Target_order)
                Target_order.is_payment_completed = True
                Target_order.save()
                logger.info(f"Payment status updated: {payment.id} -> {payment.status}")
                # return Response({"message": "Payment status updated successfully."},
                #  status.HTTP_200_OK)

                print(f"Payment status updated: {payment.id} -> {payment.status}")
                return redirect(constant.CALL_BACK_URL)

            else:
                logger.info(
                    f"Payment failed or not completed: {payment.id} -> {payment.status}"
                )
                # return Response({"message": "Payment not completed, booking cancelled."},
                #  status=status.HTTP_200_OK)
                order_tasks.confirm_or_cancel_temporary_bookings(Target_order, False)
                print(f"Payment status updated: {payment.id} -> {payment.status}")
                return redirect(constant.CALL_BACK_URL)
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        # return Response({"error": "An unexpected error occurred."}, 
        # status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return redirect(constant.CALL_BACK_URL)


"""

from abc import ABC, abstractmethod

# Step 1: Define an abstract base class for payment processing
class PaymentStrategy(ABC):
    @abstractmethod
    def create_source(self, request_data):
        pass

# Step 2: Implement concrete classes for each payment method
class CreditCardPayment(PaymentStrategy):
    def create_source(self, request_data):
        return {
            'type': 'creditcard',
            'name': request_data['source']['name'],
            'number': request_data['source']['number'],
            'cvc': request_data['source']['cvc'],
            'month': request_data['source']['month'],
            'year': request_data['source']['year']
        }

class StcPayPayment(PaymentStrategy):
    def create_source(self, request_data):
        return {
            'type': 'stcpay',
            'mobile': request_data['source']['mobile']
        }

class ApplePayPayment(PaymentStrategy):
    def create_source(self, request_data):
        return {
            'type': 'applepay',
            'token': request_data['source']['token']
        }

# Step 3: Modify the create_moyasar_payment function to use the strategy pattern
def create_moyasar_payment(request_data, validated_data, Target_order):
    api_key = settings.SECRET_KEY
    encoded_api_key = base64.b64encode(api_key.encode()).decode()
    headers = {
        'Authorization': f'Basic {encoded_api_key}',
        'Content-Type': 'application/json',
    }

    # Create a map of payment types to their respective strategies
    payment_strategies = {
        'creditcard': CreditCardPayment(),
        'stcpay': StcPayPayment(),
        'applepay': ApplePayPayment(),
    }

    # Get the payment strategy based on the source type
    source_type = request_data['source']['type']
    payment_strategy = payment_strategies.get(source_type)

    if not payment_strategy:
        return None, Response({"error": "Unsupported payment type"},
          status=status.HTTP_400_BAD_REQUEST)

    # Use the strategy to create the source
    source = payment_strategy.create_source(request_data)
    
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


"""
