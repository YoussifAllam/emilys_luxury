from apps.orders.models import Order , OrderItem , OrderDetails
from rest_framework.status import HTTP_200_OK ,HTTP_400_BAD_REQUEST , HTTP_404_NOT_FOUND

from apps.investment.models import investmenter_details, investmenter_balance , investmenter_dresses

def get_user_orders_details(request):
    user_orders = Order.objects.filter(user=request.user, is_payment_completed=True)
    
    if not user_orders.exists():
        return None, HTTP_404_NOT_FOUND
    
    order_details = OrderDetails.objects.filter(order__in=user_orders)
    return order_details, HTTP_200_OK


def get_investor_dresses(request):
    try:
        investor_dresses = investmenter_dresses.objects.filter(user=request.user)
        return investor_dresses , HTTP_200_OK
    except investmenter_dresses.DoesNotExist:
        return {'status': 'fialed' , 'error': 'this investor does not have any dresses'}, HTTP_404_NOT_FOUND
    
def get_investor_balance(request):
    try:
        investor_balance = investmenter_balance.objects.get(user=request.user)
        # return {'curr_balance' : investor_balance.curr_balance ,
        #          'total_balance' : investor_balance.total_balance} , HTTP_200_OK
        return {'balance' : investor_balance} , HTTP_200_OK
    
    except investmenter_balance.DoesNotExist:
        return {'status': 'fialed' , 'error': 'this investor does not have any balance'}, HTTP_404_NOT_FOUND