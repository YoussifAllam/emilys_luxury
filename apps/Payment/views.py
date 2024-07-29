from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Payment
from .serializers import InputSerializers
import logging
logger = logging.getLogger(__name__)

from .Tasks import pay_tasks 
from .db_services import services
class CreatePaymentView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = InputSerializers.PaymentSerializer(data=request.data)
        if serializer.is_valid():
            payment_id, response = pay_tasks.create_moyasar_payment(request.data, serializer.validated_data)
            if response.status_code == 201 and payment_id:

                services.create_payment_object(payment_id, serializer.validated_data)

                payment_response = response.json()
                transaction_url = payment_response.get('transaction_url')
                if transaction_url:
                    return Response({"transaction_url": transaction_url}, status=status.HTTP_200_OK)
                else:
                    return Response(payment_response, status=status.HTTP_201_CREATED)
                
            logger.error(f"Failed to create Moyasar payment: {response.json()}")
            return Response(response.json(), status=response.status_code)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    


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
         


