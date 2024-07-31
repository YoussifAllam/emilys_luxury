from apps.orders import models as order_models
# from apps.Payment import models as payment_models
# from apps.Shipping import models as shipping_models
# from apps.investment import models as investmenter_models
# from apps.Users.models import User as User_model
from apps.Dresses import models as Dress_model
from rest_framework.status import HTTP_200_OK ,HTTP_400_BAD_REQUEST
# from ..db_services import selectors
from django.db.models import Q 
from django.db import transaction
from typing import Dict

@transaction.atomic
def create_busy_days_for_order(order: order_models.Order)-> tuple[Dict , int]:
    """
    For each item in the given order, fetch the booking days and create dress_busy_days objects.
    """
    try:
        for item in order.items_set.all():
            booking_days = order_models.order_dress_booking_days.objects.filter(Q(OrderItem=item) & Q(dress=item.Target_dress))
            
            for booking_day in booking_days:
                Dress_model.dress_busy_days.objects.create(
                    dress=booking_day.dress,
                    busy_day=booking_day.day
                )
        return ({'status': 'success' }, HTTP_200_OK)
    
    except Exception as e:
        # Optionally log the exception here
        return ({'status': 'failed',
                  'error': 'The booking days are not available',
                #   'exception': str(e)
                 }
                , HTTP_400_BAD_REQUEST)

