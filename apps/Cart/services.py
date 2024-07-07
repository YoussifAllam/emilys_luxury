from .models import Cart_Items
from datetime import datetime
from apps.Shipping.models import Shipping


def get_Shipping_Flat_rate():
    Shipping_rate = Shipping.objects.get(id = 1)
    return Shipping_rate.flatRate

def Check_if_Cart_Item_Exists(cart_id, dress_id):
    try:
        cart_items = Cart_Items.objects.get(cart_id=cart_id, dress=dress_id)
        return True , cart_items
    except Cart_Items.DoesNotExist:
        return False , None
    
def calculate_total_price(cart_items ):
    total_price = 0
    Subtotal = 0
    for item in cart_items:
        sale_price = item.product_size.Product_sale_price
        regular_price = item.product_size.Product_regular_price
        if sale_price != 0 :
            Subtotal += sale_price * item.quantity
        else : 
            Subtotal += regular_price * item.quantity

        Shipping_Flat_rate = get_Shipping_Flat_rate()
        total_price = Subtotal + Shipping_Flat_rate
    return  Subtotal , total_price , Shipping_Flat_rate
    
def calc_total_price_with_coupon(Subtotal, coupon):
    valid_to = coupon.valid_to.date()  # Convert to date
    discount = coupon.discount
    today_date = datetime.today().date()

    Shipping_Flat_rate = get_Shipping_Flat_rate()


    if valid_to >= today_date:
        Subtotal -= (Subtotal * (discount / 100))
        total_price = Subtotal + Shipping_Flat_rate
        return Subtotal,total_price ,  True
    else:
        return Subtotal, 0 , False