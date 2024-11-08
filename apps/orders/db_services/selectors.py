from apps.Cart.models import Cart
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from ..models import Order, OrderDetails

# from apps.Dresses.models import Dresses as Dresses_model
from apps.Coupons.models import Coupon
from apps.Shipping.models import Shipping
from apps.Payment.models import Payment


def get_cart(request):
    cart_uuid = request.GET.get("cart_uuid")
    if not cart_uuid:
        return (
            {"status": "failed", "error": "cart_uuid is required"},
            HTTP_400_BAD_REQUEST,
        )
    try:
        Target_cart = Cart.objects.get(id=cart_uuid)
        return ({"status": "success", "Target_cart": Target_cart}, HTTP_200_OK)
    except Cart.DoesNotExist:
        return ({"status": "failed", "error": "Cart not found"}, HTTP_404_NOT_FOUND)


def get_order(data):
    order_uuid = data["uuid"]
    Target_order = Order.objects.get(uuid=order_uuid)
    return Target_order


def get_order_uuig_regquest_get(request):
    order_uuid = request.GET.get("uuid")
    if not order_uuid:
        return ({"status": "failed", "error": "uuid is required"}, HTTP_400_BAD_REQUEST)
    try:
        Target_order = Order.objects.get(uuid=order_uuid)
    except Order.DoesNotExist:
        return ({"status": "failed", "error": "Order not found"}, HTTP_404_NOT_FOUND)
    return ({"status": "success", "Target_order": Target_order}, HTTP_200_OK)


def get_order_using_request(request):
    order_uuid = request.data.get("uuid")
    if not order_uuid:
        return ({"status": "failed", "error": "uuid is required"}, HTTP_400_BAD_REQUEST)
    try:
        Target_order = Order.objects.get(uuid=order_uuid)
    except Order.DoesNotExist:
        return ({"status": "failed", "error": "Order not found"}, HTTP_404_NOT_FOUND)
    return ({"status": "success", "Target_order": Target_order}, HTTP_200_OK)


def get_order_items(requset):
    data, status = get_order_using_request(requset)
    if status == HTTP_200_OK:
        order = data["Target_order"]
        order_items = order.items.all()
        return ({"status": "success", "order_items": order_items}, HTTP_200_OK)
    return (data, status)


def get_user_orders(request):
    user = request.user
    orders = user.user_orders_set.all()
    return ({"status": "success", "orders": orders}, HTTP_200_OK)


def get_dress_booking_price(booking_for_n_days, dress):
    if booking_for_n_days == 3:
        return dress.price_for_3days, True

    elif booking_for_n_days == 6:
        return dress.price_for_6days, True

    elif booking_for_n_days == 8:
        return dress.price_for_8days, True

    return 0, False


def get_coupon(coupon_code):
    try:
        coupon = Coupon.objects.get(code=coupon_code)
        return ({"status": "success", "coupon": coupon}, HTTP_200_OK)
    except Coupon.DoesNotExist:
        return ({"status": "fialed", "error": "Coupon not found"}, HTTP_404_NOT_FOUND)


def get_shipping_price():
    shipping_price = Shipping.objects.first().flatRate
    return shipping_price


def get_order_details_object(order):
    try:
        OrderDetails_obj = OrderDetails.objects.get(order=order)
        pass
    except OrderDetails.DoesNotExist:
        return (
            {"status": "failed", "error": "Order details not found"},
            HTTP_404_NOT_FOUND,
        )
    return ({"OrderDetails": OrderDetails_obj}, HTTP_200_OK)


def get_order_details_obj(request):
    try:
        OrderDetails_obj = OrderDetails.objects.get(order=request.data.Get("uuid"))
        pass
    except OrderDetails.DoesNotExist:
        return (
            {"status": "failed", "error": "Order details not found"},
            HTTP_404_NOT_FOUND,
        )
    return ({"OrderDetails": OrderDetails_obj}, HTTP_200_OK)


def get_payment_instnace(order):
    try:
        Payment_obj = Payment.objects.get(order_uuid=order.uuid)
        return Payment_obj
    except Payment.DoesNotExist:
        return None
