from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from ..serializers import InputSerializers
from . import selectors
from ..models import order_dress_booking_days, OrderItem, Order
from datetime import timedelta
from django.http import HttpRequest
from typing import Tuple, Dict
from apps.Coupons.models import Coupon as Coupon_model


def create_order(request: HttpRequest, total_price: int):
    Target_data = request.data.copy()
    Target_data["user"] = request.user.id
    Target_data["total_price"] = total_price
    coupon_code = request.data.get("coupon", None)
    Target_data["applied_coupon"] = coupon_code
    delete_coupon(coupon_code)
    serializer = InputSerializers.AddOrderSerializer(data=Target_data)
    if serializer.is_valid():
        serializer.save()
        return (serializer.data, HTTP_201_CREATED)
    else:
        return (serializer.errors, HTTP_400_BAD_REQUEST)


def create_order_items(data, Target_cart):
    target_order = selectors.get_order(data)
    target_cart_items = Target_cart.items_set.all()
    for item in target_cart_items:
        price = selectors.get_dress_booking_price(item.booking_for_n_days, item.dress)[
            0
        ]
        item_data = {
            "order": target_order.uuid,
            "Target_dress": item.dress.id,
            "price": price,
            "booking_for_n_days": item.booking_for_n_days,
            "booking_start_date": item.booking_start_date,
            "booking_end_date": item.booking_end_date,
        }
        serializer = InputSerializers.AddOrderItemSerializer(data=item_data)
        if serializer.is_valid():
            order_item = serializer.save(order=target_order)
            add_order_dress_booking_days(order_item)
        else:
            return (
                {"status": "failed", "error": serializer.errors},
                HTTP_400_BAD_REQUEST,
            )
    # Target_cart.delete()
    return ({"status": "success", "order id": target_order.uuid}, HTTP_201_CREATED)


def add_order_dress_booking_days(order_item: OrderItem):
    booking_end_date = order_item.booking_end_date

    current_date = order_item.booking_start_date
    while current_date < booking_end_date + timedelta(days=2):
        order_dress_booking_days.objects.create(
            OrderItem=order_item, dress=order_item.Target_dress, day=current_date
        )
        current_date += timedelta(days=1)


def update_order_status(request: HttpRequest):
    new_status = request.data.get("status")
    if not new_status:
        return (
            {"status": "failed", "error": "status is required"},
            HTTP_400_BAD_REQUEST,
        )

    if new_status not in ["Pending", "Processing", "Shipped", "Delivered", "Cancelled"]:
        return (
            {
                "status": "failed",
                "error": "status is invalid and should be one of these : Pending, Processing, Shipped, Delivered, Cancelled",
            },
            HTTP_400_BAD_REQUEST,
        )

    data, status = selectors.get_order_using_request(request)
    if status != HTTP_200_OK:
        return (data, status)

    target_order = data["Target_order"]
    target_order.status = new_status
    target_order.save()
    return (
        {
            "status": "success",
            "message": f"order status updated successfully with uuid : {target_order.uuid}",
        },
        HTTP_200_OK,
    )


def create_order_detail(request: HttpRequest, target_order: Order) -> Tuple[Dict, int]:
    new_data = request.data.copy()
    new_data["order"] = target_order.uuid
    serializer = InputSerializers.OrederDetailSerializer(data=new_data)
    if serializer.is_valid():
        serializer.save()
        return ({"status": "succes", "data": serializer.data}, HTTP_201_CREATED)
    else:
        return (serializer.errors, HTTP_400_BAD_REQUEST)


def delete_coupon(coupon_code: str):
    try:
        coupon = Coupon_model.objects.get(code=coupon_code)
        coupon.delete()
    except Coupon_model.DoesNotExist:
        pass
