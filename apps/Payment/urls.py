from django.urls import path
from .views import CreatePaymentView ,PaymentCallbackView,payment

urlpatterns = [
    path('create/', CreatePaymentView.as_view(), name='create_payment'),
    path('callback/', PaymentCallbackView.as_view(), name='create_payment'),
    path('payments/',payment.as_view(), name='payments'),
]
