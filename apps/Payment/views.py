from rest_framework.status import HTTP_200_OK , HTTP_201_CREATED ,HTTP_400_BAD_REQUEST , HTTP_404_NOT_FOUND
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Payment
from .serializers import InputSerializers
from .Tasks import order_tasks , payout_tasks
from .db_services import selectors
import logging
logger = logging.getLogger(__name__)
from .Tasks import pay_tasks 
from rest_framework.permissions import IsAuthenticated


from apps.investment.models import investmenter_details, investmenter_balance

class CreatePaymentView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        serializer = InputSerializers.PaymentSerializer(data=request.data)
        if serializer.is_valid():
            order_uuid = serializer.validated_data['order_uuid']
            Target_order = selectors.get_order_by_uuid(order_uuid)
            if not Target_order: return Response({'status': 'failed','error': 'order not found'}, status=HTTP_400_BAD_REQUEST)

            Response_data , Response_status = order_tasks.create_busy_days_for_order(Target_order)
            if Response_status != HTTP_200_OK :
                return Response(Response_data , Response_status)
            
            payment_id,order_uuid , response = pay_tasks.create_moyasar_payment(request.data, serializer.validated_data , Target_order)
            if response.status_code == 201 and payment_id:

                payment_response = response.json()
                transaction_url = payment_response.get('transaction_url')
                if transaction_url:
                    return Response({"transaction_url": transaction_url}, status=HTTP_200_OK)
                else:
                    return Response(payment_response, status=HTTP_201_CREATED)
                
            logger.error(f"Failed to create Moyasar payment: {response.json()}")
            return Response(response.json(), status=response.status_code)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class TransferBalanceView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        try:
            investor_details = investmenter_details.objects.get(user=user)
            investor_balance = investmenter_balance.objects.get(user=user)
        except investmenter_details.DoesNotExist:
            return Response({"error": "Investor details not found"}, status=HTTP_404_NOT_FOUND)
        except investmenter_balance.DoesNotExist:
            return Response({"error": "Investor balance not found"}, status=HTTP_404_NOT_FOUND)
        
        if investor_balance.curr_balance <= 0:
            return Response({"error": "Insufficient balance"}, status=HTTP_400_BAD_REQUEST)
        
        response = payout_tasks.create_moyasar_payout(investor_details, investor_balance.curr_balance)

        if response.status_code == 201:
            payout_response = response.json()
            investor_balance.curr_balance = 0
            investor_balance.save()
            return Response(payout_response, status=HTTP_201_CREATED)
        else:
            return Response(response.json(), status=response.status_code)

class PaymentCallbackView(APIView):
    def get(self, request, *args, **kwargs):
        return pay_tasks.process_callback(request)

    def post(self, request, *args, **kwargs):
        return pay_tasks.process_callback(request)

class payment(APIView):
    def get(self, request):
        payments = Payment.objects.all()
        serializer = InputSerializers.PaymentSerializer(payments, many=True)
        return Response(serializer.data)
         

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import requests
from django.conf import settings
import base64
class vendor_transfer(APIView):
    def post(self , request):
        if request.method == 'POST':
            user = request.user
            balance = get_object_or_404(investmenter_balance, user=user)
            details = get_object_or_404(investmenter_details, user=user)
            
            transfer_amount = balance.curr_balance
            if transfer_amount <= 0:
                return JsonResponse({'error': 'Insufficient balance'}, status=400)
            
            # Perform the transfer using Moyasar API
            api_key = settings.SECRET_KEY
            encoded_api_key = base64.b64encode(api_key.encode()).decode()
            
            response = requests.post(
                'https://api.moyasar.com/v1/payouts',
                headers = {
                'Authorization': f'Basic {encoded_api_key}',
                'Content-Type': 'application/json',
            },
                json={
                    'amount': transfer_amount,
                    'currency': 'SAR',
                    'source': {
                        'type': 'creditcard',
                        'name': details.account_owner_name,
                        'number': details.credit_card_number,
                        'cvc': '123',  # Replace with the real CVC
                        'month': '01',  # Replace with the real expiry month
                        'year': '25',  # Replace with the real expiry year
                    },
                    'destination': {
                        'iban': details.iban,
                    }
                }
            )
            
            if response.status_code == 200:
                # Update balance after successful transfer
                balance.total_balance -= transfer_amount
                balance.curr_balance = 0
                balance.save()
                return JsonResponse({'message': 'Transfer successful'}, status=200)
            else:
                return JsonResponse({'error': 'Transfer failed', 'details': response.json()}, status=400)

        return JsonResponse({'error': 'Invalid request method'}, status=400)

