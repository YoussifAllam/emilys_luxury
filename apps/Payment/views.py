from rest_framework.status import HTTP_200_OK , HTTP_201_CREATED ,HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Payment
from .serializers import InputSerializers
from .Tasks import order_tasks
from .db_services import selectors
import logging
logger = logging.getLogger(__name__)

from .Tasks import pay_tasks 
from .db_services import services
class CreatePaymentView(APIView):
    
    def post(self, request, *args, **kwargs):
        serializer = InputSerializers.PaymentSerializer(data=request.data)
        if serializer.is_valid():

            """
            do_related_tasks_for_order
            this function will will pass for each dress in order and calc the investmenter new curr_balance 
            and create objects for dress booking days 
            """
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
         


