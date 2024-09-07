from apps.orders.models import Order ,  OrderDetails
from rest_framework.status import HTTP_200_OK  , HTTP_404_NOT_FOUND
from apps.Dresses.models import  Dresses 
from apps.investment.models import  investmenter_balance , investmenter_dresses

def get_user_orders_details(request):
    user_orders = Order.objects.filter(
        user=request.user, 
        is_payment_completed=True
    )
    
    if not user_orders.exists():
        return None, HTTP_404_NOT_FOUND
    
    order_details = OrderDetails.objects.filter(
        order__in=user_orders
    )

    unique_order_details = list(
        {detail.street_address: detail for detail in order_details}.values()
    )

    return unique_order_details, HTTP_200_OK


def get_investor_dresses(request):
    try:
        investor_dresses = investmenter_dresses.objects.filter(user=request.user)
        return investor_dresses , HTTP_200_OK
    except investmenter_dresses.DoesNotExist:
        return {'status': 'fialed' , 'error': 'this investor does not have any dresses'}, HTTP_404_NOT_FOUND
    
def get_investor_balance(request):
    try:
        investor_balance = investmenter_balance.objects.get(user=request.user)
        return {'balance' : investor_balance} , HTTP_200_OK
    
    except investmenter_balance.DoesNotExist:
        return {'status': 'fialed' , 'error': 'this investor does not have any balance'}, HTTP_404_NOT_FOUND
    
def get_dress_using_uuid(dress_uuid) -> Dresses:
    try:
        return Dresses.objects.get(id=dress_uuid)
    except Dresses.DoesNotExist:
        return None
    