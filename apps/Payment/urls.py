from django.urls import path
from .views import (
    CreatePaymentView,
    PaymentCallbackView,
    payment,
    PayoutView,
    RefundView,
)

urlpatterns = [
    path("create/", CreatePaymentView.as_view(), name="create_payment"),
    path("callback/", PaymentCallbackView.as_view(), name="create_payment"),
    path("Payout/", PayoutView.as_view(), name="transfer-balance"),
    path("payments/", payment.as_view(), name="payments"),
    path("refund/", RefundView.as_view(), name="refund"),
]
