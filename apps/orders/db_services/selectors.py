from apps.Cart.models import Cart
from rest_framework.status import HTTP_200_OK ,HTTP_400_BAD_REQUEST , HTTP_404_NOT_FOUND 
from ..models import Order 


def get_cart(request):
    cart_uuid = request.data.get('cart_uuid')
    if not cart_uuid:
        return ({'status': 'failed','error': 'cart_uuid is required'}, HTTP_400_BAD_REQUEST)
    try:
        Target_cart = Cart.objects.get(id=cart_uuid)
        return ({'status': 'success', 'Target_cart': Target_cart}, HTTP_200_OK)
    except Cart.DoesNotExist:
        return({'status': 'failed','error' : 'Cart not found'} , HTTP_404_NOT_FOUND)
    
def get_order(data):
    order_uuid = data['uuid']
    Target_order = Order.objects.get(uuid=order_uuid)
    return (Target_order)
   
def get_order_using_request(request):
    order_uuid = request.data.get('uuid')
    if not order_uuid:
        return ({'status': 'failed','error': 'order_uuid is required'}, HTTP_400_BAD_REQUEST)
    try :
        Target_order = Order.objects.get(uuid=order_uuid)
    except Order.DoesNotExist:
        return ({'status': 'failed','error' : 'Order not found'} , HTTP_404_NOT_FOUND)
    return ( {'status': 'success', 'Target_order': Target_order}, HTTP_200_OK)

def get_order_items(requset):
    data , status = get_order_using_request(requset)
    if status == HTTP_200_OK:
        order = data['Target_order']
        order_items = order.items.all()
        return ({'status': 'success', 'order_items': order_items}, HTTP_200_OK)
    return (data , status)

def get_user_orders(request):
    user = request.user
    orders = user.user_orders_set.all()
    return ({'status': 'success', 'orders': orders}, HTTP_200_OK)

