from apps.orders import models as order_models
from apps.Dresses import models as Dress_model
from rest_framework.status import HTTP_200_OK ,HTTP_400_BAD_REQUEST
from django.db import transaction
from typing import Dict
from datetime import timedelta

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
                Dress_model.dress_busy_days.objects.create(dress=dress, busy_day=single_date, is_temporary=True)
                update_dress_Num_of_rentals(dress)
    
        return ({'status': 'success' }, HTTP_200_OK)
    
    except Exception as e:
        return ({'status': 'failed',
                  'error': 'The booking days are not available',
                #   'exception': str(e)
                 }
                , HTTP_400_BAD_REQUEST)

def confirm_or_cancel_temporary_bookings(order, is_success):
    busy_days = Dress_model.dress_busy_days.objects.filter(dress__in=[item.Target_dress for item in order.items_set.all()], is_temporary=True)
    if is_success:
        busy_days.update(is_temporary=False)  # Confirm the booking
    else:
        busy_days.delete()  # Cancel the temporary booking

def update_dress_Num_of_rentals(dress):
    dress.Num_of_rentals += 1
    dress.save()