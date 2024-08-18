from apps.orders import models as order_models
from apps.Dresses import models as Dress_model
from rest_framework.status import HTTP_200_OK ,HTTP_400_BAD_REQUEST
from django.db import transaction
from typing import Dict
from datetime import timedelta , datetime
# from uuid import  uuid4
from django.http import HttpRequest
from ..serializers import params_serializer
from . import Refund_tasks , investor_balance_tasks
from ..db_services import selectors
from django.utils import timezone

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days) + 2): # is +2 becuase we need 2 days after booking end date for washing and dry the dress
        yield start_date + timedelta(n)

@transaction.atomic
def create_busy_days_for_order(order: order_models.Order)-> tuple[Dict , int]:
    """
    For each item in the given order, fetch the booking days and create dress_busy_days objects.
    """
    try:
        for item in order.items_set.all():
            dress = item.Target_dress
            for single_date in daterange(item.booking_start_date, item.booking_end_date):
                Dress_model.dress_busy_days.objects.create(dress=dress, busy_day=single_date, is_temporary=True ,order_uuid = order.uuid) 
                update_dress_Num_of_rentals(dress)
    
        return ({'status': 'success' }, HTTP_200_OK)
    
    except Exception as e:
        return ({'status': 'failed',
                  'error': 'The booking days are not available',
                #   'exception': str(e)
                 }
                , HTTP_400_BAD_REQUEST)

def confirm_or_cancel_temporary_bookings(order, is_success):
    busy_days = Dress_model.dress_busy_days.objects.filter(dress__in=[item.Target_dress for item in order.items_set.all()],
                                                            is_temporary=True , order_uuid = order.uuid)
    # print(busy_days , '+++++++++++')
    if not busy_days:
        return None
    if is_success:
        busy_days.update(is_temporary=False)  # Confirm the booking
    else:
        busy_days.delete()  # Cancel the temporary booking

    return True

def update_dress_Num_of_rentals(dress):
    dress.Num_of_rentals += 1
    dress.save()

def check_if_order_is_able_to_refund(target_order : order_models.Order) -> tuple[bool, str]:
    if target_order.status == 'Cancelled' or target_order.status == 'Delivered':
        return (
            {'status': 'failed', 'error': 'The order is already cancelled or delivered'},
            HTTP_400_BAD_REQUEST
        )

    if target_order.is_payment_completed == False:
        return (
            {'status': 'failed', 'error': 'The order is not paid yet'},
            HTTP_400_BAD_REQUEST
        )

    return (True, 'success')

def hours_until_arrival(target_order : order_models.Order) -> float:
        arrival_date = target_order.arrival_date
        if arrival_date :
            now = timezone.now()

            # Combine arrival_date with the minimum time to create a datetime object
            arrival_datetime = timezone.make_aware(datetime.combine(arrival_date, datetime.min.time()))

            # Calculate the difference between arrival_datetime and now
            time_difference = arrival_datetime - now

            # Convert the time difference to hours
            hours_until_arrival = time_difference.total_seconds() / 3600
            return False , hours_until_arrival
        
        return True , 0 # arrival_date not set yet
    
def get_amount_to_refund(target_order : order_models.Order) -> tuple[Dict, str]:
    vaild , hours = hours_until_arrival(target_order)
    print(hours , 15*"8")
    amount_60 = int(target_order.total_price * 0.60)
    if vaild: # arrival_date not set yet
        return amount_60
    
    if hours > 50:
        return amount_60
    
    else : # hours < 50
        amount_30 = int(target_order.total_price * 0.30)
        return amount_30
    
def delete_item_booking_days(item : order_models.OrderItem):
    start_date = item.booking_start_date
    end_date = item.booking_end_date
    for single_date in daterange(start_date, end_date):
        try:
            dress_busy_day = Dress_model.dress_busy_days.objects.get(dress=item.Target_dress, busy_day=single_date)
            dress_busy_day.delete()
        except Exception as e:
            print(e)
    
def update_order_realted_data(target_order : order_models.Order):
    target_order.is_payment_completed = False
    target_order.save()
    order_items = target_order.items_set.all()
    for item in order_items:
        investor_balance_tasks.reduce_investor_balance(item)
        delete_item_booking_days(item)

def Refund_order(request: HttpRequest) -> tuple[Dict, int]:
    serializer = params_serializer.Check_vaild_refund_params(data=request.data)
    if not serializer.is_valid():
        return (
            {'status': 'failed', 'error': serializer.errors},
            HTTP_400_BAD_REQUEST
        )
    
    order_id = serializer.data['order_id']
    target_order = selectors.get_order_by_uuid(order_id)
    if not target_order:
        return (
            {'status': 'failed', 'error': 'The order does not exist'},
            HTTP_400_BAD_REQUEST
        )

    is_vaild , vaild_error = check_if_order_is_able_to_refund(target_order)
    if not is_vaild:
        return (
            {'status': 'failed', 'error': vaild_error},
            HTTP_400_BAD_REQUEST
        )
    
    payment_id = selectors.get_payment_id(target_order)
    if not  payment_id:
        return (
            {'status': 'failed', 'error': 'The order is not paid yet'},
        )

    amount_to_refund = get_amount_to_refund(target_order) 
    response_data, response_status = Refund_tasks.refund_moyasar_order(
        payment_id, amount_to_refund, order_id
    )
    if response_status == HTTP_200_OK:
        update_order_realted_data(target_order)
    return (response_data, response_status)


