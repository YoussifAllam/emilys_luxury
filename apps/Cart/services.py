from .models import Cart_Items
from datetime import datetime
from apps.Shipping.models import Shipping , INSURANCE


def get_Shipping_and_INSURANCE_rate():
    Shipping_rate = Shipping.objects.get(id = 1)
    INSURANCE_rate = INSURANCE.objects.get(id = 1)
    return Shipping_rate.flatRate , INSURANCE_rate.INSURANCE

def Check_if_Cart_Item_Exists(cart_id, dress_id):
    try:
        cart_items = Cart_Items.objects.get(cart_id=cart_id, dress=dress_id)
        return True , cart_items
    except Cart_Items.DoesNotExist:
        return False , None
    
def get_dress_price( obj):
        booking_days = int(obj.booking_for_n_days)
        if booking_days == 3:
            return obj.dress.price_for_3days
        elif booking_days == 6:
            return obj.dress.price_for_6days
        elif booking_days == 8:
            return obj.dress.price_for_8days
        return None

def calculate_total_price(cart_items ):
    total_price = 0
    Subtotal = 0
    for item in cart_items:
        price = get_dress_price(item)
        Subtotal+=price

    Shipping_Flat_rate , INSURANCE_rate = get_Shipping_and_INSURANCE_rate()
    total_price = Subtotal + Shipping_Flat_rate  
    return  Subtotal , total_price , Shipping_Flat_rate , INSURANCE_rate
    
def calc_total_price_with_coupon(Subtotal, coupon):
    valid_to = coupon.valid_to.date()  # Convert to date
    discount = coupon.discount
    today_date = datetime.today().date()

    Shipping_Flat_rate , INSURANCE_rate = get_Shipping_and_INSURANCE_rate()


    if valid_to >= today_date:
        Subtotal -= (Subtotal * (discount / 100))
        total_price = Subtotal + Shipping_Flat_rate  
        return Subtotal,total_price ,  True
    else:
        return Subtotal, 0 , False
    
