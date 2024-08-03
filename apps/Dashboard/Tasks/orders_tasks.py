from ..db_services import selectors


def get_order_shipping_address(request):
    response_data , response_status = selectors.get_user_orders_details(request)
    return response_data , response_status
    
    