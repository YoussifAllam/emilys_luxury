from django.urls import path
from .views import CreatePaymentView , PaymentCallbackView , payment ,TransferBalanceView ,vendor_transfer

urlpatterns = [
    path('create/', CreatePaymentView.as_view(), name='create_payment'),
    path('callback/', PaymentCallbackView.as_view(), name='create_payment'),
    path('transfer-balance/', TransferBalanceView.as_view(), name='transfer-balance'),
    path('payments/',payment.as_view(), name='payments'),
    path('vendor_transfer/' , vendor_transfer.as_view())
]
