from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Payment
from .serializers import InputSerializers
from .Tasks import order_tasks, payout_tasks
from .db_services import selectors
import logging
from .Tasks import pay_tasks
from rest_framework.permissions import IsAuthenticated
from apps.investment.models import investmenter_details, investmenter_balance

logger = logging.getLogger(__name__)


class CreatePaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # return Response(
        #     "the payment is not allowed now come later", status=HTTP_400_BAD_REQUEST
        # )
        serializer = InputSerializers.PaymentSerializer(data=request.data)
        if serializer.is_valid():
            order_uuid = serializer.validated_data["order_uuid"]
            Target_order = selectors.get_order_by_uuid(order_uuid)
            if not Target_order:
                return Response(
                    {"status": "failed", "error": "order not found"},
                    status=HTTP_400_BAD_REQUEST,
                )

            if not order_tasks.booking_days_is_available(Target_order):
                return Response(
                    {"status": "failed", "error": "booking days are not available"},
                    status=HTTP_400_BAD_REQUEST,
                )

            if not order_tasks.all_order_items_are_available(Target_order):
                return Response(
                    {"status": "failed", "error": "booking days are not available"},
                    status=HTTP_400_BAD_REQUEST,
                )

            payment_id, order_uuid, response = pay_tasks.create_moyasar_payment(
                request.data, serializer.validated_data, Target_order
            )
            if response.status_code == 201 and payment_id:
                Response_data, Response_status = order_tasks.create_busy_days_for_order(
                    Target_order
                )
                if Response_status != HTTP_200_OK:
                    return Response(Response_data, Response_status)
                payment_response = response.json()
                source = payment_response.get("source")
                transaction_url = source["transaction_url"]
                if transaction_url:
                    # print('transaction_url : ',transaction_url , '\n')
                    return Response(
                        {"transaction_url": transaction_url}, status=HTTP_201_CREATED
                    )

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


class PayoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        try:
            investor_details = investmenter_details.objects.get(user=user)
            investor_balance = investmenter_balance.objects.get(user=user)
        except investmenter_details.DoesNotExist:
            return Response(
                {"error": "Investor details not found"}, status=HTTP_404_NOT_FOUND
            )
        except investmenter_balance.DoesNotExist:
            return Response(
                {"error": "Investor balance not found"}, status=HTTP_404_NOT_FOUND
            )

        if investor_balance.curr_balance <= 0:
            return Response(
                {"error": "Insufficient balance"}, status=HTTP_400_BAD_REQUEST
            )

        response = payout_tasks.create_moyasar_payout(
            investor_details, investor_balance.curr_balance
        )

        if response.status_code == 201:
            payout_response = response.json()
            investor_balance.curr_balance = 0
            investor_balance.save()
            return Response(payout_response, status=HTTP_201_CREATED)
        else:
            return Response(response.json(), status=response.status_code)


class RefundView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        Response_data, Response_status = order_tasks.Refund_order(request)
        return Response(Response_data, status=Response_status)


# get all payments
class payment(APIView):
    def get(self, request):
        payments = Payment.objects.all()
        serializer = InputSerializers.PaymentSerializer(payments, many=True)
        return Response(serializer.data)


class check_payment_status_view(APIView):
    def get(self, request):
        payment_uuid = request.GET.get("uuid")
        is_paid = pay_tasks.chack_if_payment_completed(payment_uuid)

        if is_paid is None:
            return Response(
                {"status": "error", "message": "Payment not found or error occurred."}
            )
        elif is_paid:
            return Response({"status": "success", "message": "Payment is completed."})
        else:
            return Response(
                {"status": "pending", "message": "Payment is not completed yet."}
            )
