from django.urls import path  # ,include
from .views import *

# url_domain_a = []

urlpatterns = [
    # path('domain_a/', include(url_domain_a)),
    path("Order/", Order.as_view(), name="order_create"),
    path("OrderItems/", OrderItems.as_view(), name="order_items"),
    path("order_details/", OrderDetails.as_view(), name="order_details"),
    path("get_user_orders/", get_user_orders),
    path("track_order/", track_order),
    path("order_billing_details/", Get_Put_order_details.as_view()),
]
