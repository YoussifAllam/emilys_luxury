from rest_framework.status import HTTP_200_OK , HTTP_201_CREATED ,HTTP_400_BAD_REQUEST 
from ..db_services import selectors
from datetime import timedelta , datetime

def Calculate_total_price(data , request ):
    Target_cart = data['Target_cart']
    cart_items = Target_cart.items_set.all()
    if not cart_items :
        return ( 0, 0,  {'status': 'failed', 'error': 'Cart is empty'} , HTTP_400_BAD_REQUEST)
    
    total_price = 0
    for item in cart_items:
        if not booking_days_is_available(item): 
            return ( 0, 0,  {'status': 'failed', 'error': f'the booking days for dress is not available'} , HTTP_400_BAD_REQUEST)
        
        booking_price , is_succes = selectors.get_dress_booking_price(item.booking_for_n_days , item.dress)
        if not is_succes: return ( 0, 0,  {'status': 'failed', 'error': 'booking price not found'} , HTTP_400_BAD_REQUEST)

        total_price += booking_price
        
        if request.data.get('coupon' , None):
            total_price , is_succes = calc_total_price_with_coupon(total_price, request.data.get('coupon'))
            if not is_succes: return ( 0, 0,  {'status': 'failed', 'error': 'coupon not valid'} , HTTP_400_BAD_REQUEST)
        
        total_price += selectors.get_shipping_price()
        
    return ( total_price , Target_cart , {'status': 'success', 'total_price': total_price } , HTTP_200_OK)

def booking_days_is_available(item):
    dress = item.dress
    booking_start_date = item.booking_start_date
    booking_end_date = item.booking_end_date
    busy_days = dress.busy_day_set.values_list('busy_day', flat=True)
    
    current_date = booking_start_date
    while current_date <= booking_end_date:
        if current_date in busy_days:
            return False
        current_date += timedelta(days=1)
    return True
     
def calc_total_price_with_coupon(Subtotal, coupon_code):
    data ,status = selectors.get_coupon(coupon_code)
    if status != HTTP_200_OK:
        return  0 , False
    coupon = data['coupon']
    valid_to = coupon.valid_to.date()  # Convert to date
    discount = coupon.discount
    today_date = datetime.today().date()


    if valid_to >= today_date:
        Subtotal -= (Subtotal * (discount / 100))
        return Subtotal ,  True
    else:
        return  0 , False



