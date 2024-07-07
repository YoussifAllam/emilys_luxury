from django.urls import path 
from .views import *
urlpatterns = [

    path('create_cart/', create_cart),
    path('add_item/', add_item),
    path('get_cart_details/', get_cart_details),
    path('remove_item_from_cart/'  ,remove_item_from_cart),
    path('clear_shopping_cart/' , clear_shopping_cart) , 
    path('cart_total_price/' , cart_total_price)
]
