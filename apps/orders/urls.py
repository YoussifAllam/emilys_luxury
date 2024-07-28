from django.urls import path # ,include
from .views import *

# url_domain_a = []

urlpatterns = [
    # path('domain_a/', include(url_domain_a)),

    path('Order/', Order.as_view(), name='order_create'),
    path('OrderItems/' , OrderItems.as_view(), name='order_items') ,
    path('get_user_orders/' , get_user_orders)
]