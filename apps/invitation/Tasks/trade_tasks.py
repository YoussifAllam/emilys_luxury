from ..db_services import selectors , services
from django.http import HttpRequest
from rest_framework.status import HTTP_200_OK , HTTP_400_BAD_REQUEST , HTTP_201_CREATED
from apps.Coupons.models import Coupon as Coupon_model
from django.utils import timezone
from datetime import timedelta

def Trade_points(request: HttpRequest):
    user_points_obj = selectors.get_user_points(request.user)
    system_points_to_trade_obj = selectors.get_system_points_to_trade_obj()

    user_curr_points = user_points_obj.num_of_points
    reqiurd_points_for_code =  system_points_to_trade_obj.num_of_points_for_code

    if user_curr_points < reqiurd_points_for_code:
        return ({'status':'failed' , 'error' : 'your points is less than reqiurd'} , HTTP_400_BAD_REQUEST)
    
    else :
        valid_to_date = timezone.now() + timedelta(days=10)
        coupon = Coupon_model.objects.create(
            discount=system_points_to_trade_obj.discount,
            code=Coupon_model.generate_unique_code(),
            valid_to=valid_to_date
        )
       
        user_points_obj.num_of_points -= reqiurd_points_for_code
        user_points_obj.save()

        return({'status':'success' , 'coupon' : coupon.code} , HTTP_201_CREATED)
        
    
    
