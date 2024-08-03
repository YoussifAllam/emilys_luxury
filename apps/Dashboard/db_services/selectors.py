from apps.orders.models import Order , OrderItem , OrderDetails
from rest_framework.status import HTTP_200_OK ,HTTP_400_BAD_REQUEST , HTTP_404_NOT_FOUND

def get_user_orders_details(request):
    user_orders = Order.objects.filter(user=request.user, is_payment_completed=True)
    
    if not user_orders.exists():
        return None, HTTP_404_NOT_FOUND
    
    order_details = OrderDetails.objects.filter(order__in=user_orders)
    return order_details, HTTP_200_OK